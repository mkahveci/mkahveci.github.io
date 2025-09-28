# This script combines three preprocessing steps into a single, ordered workflow.
# 1. Download Readmes and supporting Docs from GitHub.
# 2. Preprocess downloaded Markdown files (add front matter, fix links).
# 3. Generate project metadata from GitHub API and save it to _data/projectsgit.yml.

# --- Global Configuration and Dependencies ---
require 'yaml'
require 'octokit'
require 'down'
require 'fileutils'

$basedir = Dir.pwd
REPO_DIR = "projectsgit" # Standardized project directory name
DATA_FILE = "_data/#{REPO_DIR}.yml"

# --- 1. README and Docs Downloader (generate-readmes.rb logic) ---

module ReadmeDownloader
    # Determines the default branch by trying both 'main' and 'master'
    def self.get_default_branch(repo)
        client = Octokit::Client.new(:netrc => true, :access_token => ENV['GITHUB_TOKEN'])
        ['main', 'master'].each do |branch_name|
            begin
                client.ref(repo, "heads/#{branch_name}")
                return branch_name
            rescue Octokit::NotFound
                next
            rescue => e
                puts "\t\tError checking branch #{branch_name}: #{e.message}"
                return 'main' # Default fallback
            end
        end
        return 'main' # Default if neither is found
    end

    # Helper function to download all files/folders recursively from a specific subdirectory
    def self.download_subdirectory_contents(repo, subdir_name, local_dir)
        client = Octokit::Client.new(:netrc => true, :access_token => ENV['GITHUB_TOKEN'])
        api_path = subdir_name
        default_branch = self.get_default_branch(repo)

        puts "\t\tChecking subdirectory: #{api_path} on branch #{default_branch}"

        contents = nil
        begin
            contents = client.contents(repo, :path => api_path, :query => { :ref => default_branch })
        rescue Octokit::NotFound
            puts "\t\t'#{api_path}' folder not found in repository. Skipping download."
            return false
        rescue => e
            puts "\t\tError fetching contents via API: #{e.message}. Skipping download."
            return false
        end


        downloaded_any = false
        if contents && !contents.empty?
            # --- API Success Path ---
            contents.each do |item|
                item_path = item.path
                local_subpath = item_path
                local_path = File.join(local_dir, local_subpath)

                if item.type == 'dir'
                    download_subdirectory_contents(repo, item_path, local_dir)
                elsif item.type == 'file'
                    downloaded_any = true
                    begin
                        github_file = Down.download(item.download_url, max_redirects: 5)
                        FileUtils.mkdir_p(File.dirname(local_path))
                        FileUtils.mv(github_file.path, local_path)
                    rescue Down::Error => e
                        puts "\t\t\tError downloading #{item.name}: #{e.message}"
                    end
                end
            end
        end
        return downloaded_any
    end

    # New: Creates a simple index.html file that redirects to the project index.
    def self.create_docs_redirect(project_name)
        redirect_html = <<~HTML
        ---
        permalink: /#{REPO_DIR}/#{project_name}/docs/
        ---
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirecting...</title>
            <!-- Redirects to the main project index -->
            <meta http-equiv="refresh" content="0; url=/#{REPO_DIR}/#{project_name}/" />
            <link rel="canonical" href="/#{REPO_DIR}/#{project_name}/">
        </head>
        <body>
            <p>This folder is for source files. Redirecting to <a href="/#{REPO_DIR}/#{project_name}/">the main project page</a>.</p>
        </body>
        </html>
        HTML

        dir = "#{REPO_DIR}/#{project_name}/docs/"
        # Ensure the directory exists
        FileUtils.mkdir_p(dir)
        # Write the redirect file
        File.write(dir + "index.html", redirect_html)
    end


    def self.generate_readmes(config_file)
       config = YAML.load_file(config_file)
       projects_array = config["readmes"] || []

       puts "1. Downloading readmes and supporting documents"

       if projects_array.length > 0
          projects_array.each do |repo|
             puts "\tProcessing repo: #{repo}"

             name = repo.split('/').drop(1).join('')
             dir = "#{REPO_DIR}/#{name}/"
             FileUtils.mkdir_p(dir)

             default_branch = self.get_default_branch(repo)

             # --- START: Download README.md and associated images (CRITICAL FIX) ---
             begin
                # Download README.md
                githubfile = Down.download(
                   "https://raw.githubusercontent.com/#{repo}/#{default_branch}/README.md",
                   max_redirects: 5
                )
             rescue Down::Error
                puts "\t\tREADME.md not found for repo. Skipping file creation."
             else
                # Process and save README
                FileUtils.mv(githubfile.path, dir+"README.md")
                File.delete(dir+"index.md") if File.exist?(dir+"index.md") # Cleanup index.md

                # Find and download image links within readme
                if File.exist?(dir+"README.md")
                   contents = File.open(dir+"README.md", "r").read
                   matchesHTML = contents.scan /<img.+src=\"([^"]+)\"/
                   matchesMD = contents.scan /\!\[[^\]]*\]\(([^)]+)\)/
                   (matchesHTML + matchesMD).each do |match|
                      imagePath = match[0]
                      imageUrl = "https://raw.githubusercontent.com/#{repo}/#{default_branch}/#{imagePath}"
                      begin
                         imageFile = Down.download(imageUrl, max_redirects: 5)
                      rescue Down::Error
                         # Image download failed; continue to next file
                      else
                         FileUtils.mkdir_p(File.dirname(dir+imagePath))
                         FileUtils.mv(imageFile.path, dir+imagePath)
                      end
                   end
                end
             end
             # --- END: Download README.md ---

             # Check if any files were downloaded into the docs folder
             files_downloaded = self.download_subdirectory_contents(repo, "docs", dir)

             # If files were downloaded, create the redirect file to handle manual URL access
             if files_downloaded
                self.create_docs_redirect(name)
             end

          end
       end
    end
end

# --- 2. Markdown Preprocessor (preprocess-markdown.rb logic) ---

module MarkdownPreprocessor
    def self.process_markdown(config_file)

       config = YAML.load_file(config_file)
       # Safely read both arrays
       all_repos = (config["projects"] || []) + (config["readmes"] || [])
       readmes_array = config["readmes"] || []

       name_to_repo = Hash.new
       all_repos.each do |repo|
          name = repo.split('/').drop(1).join('')
          name_to_repo[name] = repo
       end

       name_to_readme = Hash.new
       readmes_array.each do |repo|
          name = repo.split('/').drop(1).join('')
          name_to_readme[name] = true
       end

       puts "2. Preprocessing Markdown files (adding front matter, renaming links)"

       mdarray = Dir.glob("#{REPO_DIR}/**/*.md")

       mdarray.each { |md|

           basename = File.basename(md)
           full_directory = File.dirname(md) + "/"

           # If readme.md, rename to index.md
           if basename =~ /readme/i
              if File.exist?(full_directory + "index.html")
                 File.delete(full_directory + "index.html")
              end
              indexmd = full_directory + "index.md"
              # Renames file
              File.rename(md, indexmd)
              md = indexmd
              basename = File.basename(md)
           end

           # Get project name from directory structure
           project_name = nil
           dirarray = full_directory.split('/')
           # Find index of the root project folder
           repo_dir_index = dirarray.index(REPO_DIR)
           if repo_dir_index && dirarray.size > repo_dir_index + 1
              temp_name = dirarray[repo_dir_index + 1]
              if temp_name =~ /^[^_]/
                 project_name = temp_name
              end
           end

           repo = name_to_repo[project_name]
           within_project_directory = full_directory[/^#{REPO_DIR}\/#{project_name}\/(.*)/, 1]

           # Read contents
           contents = File.open(md, "r").read

           # --- START: Content Assembly ---
           final_content = ""

           # 1. Add YAML front matter if missing
           if contents !~ /\A(---\s*\n.*?\n?)^(---\s*$\n?)/m
              # Build Front Matter Header
              front_matter = "---"
              front_matter += "\nlayout: projectgit"
              if project_name != nil
                 title = md.sub(/^.*#{REPO_DIR}\//, '').sub(/.md$/, '').sub(/index$/, '')
                 front_matter += "\ntitle: #{title}"
                 front_matter += "\nproject: #{project_name}"
                 front_matter += "\nrepo: #{repo}"
                 front_matter += "\npermalink: /:path/:basename:output_ext"
              end
              front_matter += "\n---"
              front_matter += "\n\n"

              # Prepend Front Matter and append original contents
              final_content = front_matter + contents

           else
              # If front matter exists, use original contents
              final_content = contents
           end

           # 2. Perform all link substitutions on the full content

           # Link to MD files -> HTML files
           final_content.gsub!(/\((\S+)\.md\)/, "(\\1.html)")

           # Link to source code files -> GitHub links
           filetypes = ['pdf', 'class', 'cpp', 'h', 'hh', 'ipynb', 'jar', 'java', 'nb', 'py', 'R', 'rb', 'Rmd', 'branches', 'csv', 'fasta', 'json', 'kml', 'log', 'mcc', 'newick', 'nex', 'tsv', 'tips', 'trees', 'timeseries', 'summary', 'txt', 'xml']
           filetypes.each {|filetype|
              final_content.gsub!(/\((\S+)\.#{filetype}\)/, "(https://github.com/#{repo}/tree/master/#{within_project_directory}\\1.#{filetype})")
           }

           # If readme, replace all internal links with GitHub links (for relative path handling in the readme)
           if name_to_readme[project_name]
              # catching links that end in "/"
              final_content.gsub!(/\((?!http)(\S+\/)\)/, "(https://github.com/#{repo}/tree/master/#{within_project_directory}\\1)")
           end

           # 3. Write file back to disk (Only done once)
           File.write(md, final_content)
           # --- END: Content Assembly ---
       }
    end
end

# --- 3. Project Data Generator (generate-project-data.rb logic) ---

module DataGenerator

    def self.generate_data(config_file)

       config = YAML.load_file(config_file)
       projects_array = (config["projects"] || []) + (config["readmes"] || [])
       readmes_array = config["readmes"] || []

       puts "3. Generating project metadata from GitHub API"
       client = Octokit::Client.new(:netrc => true, :access_token => ENV['GITHUB_TOKEN'])

       project_data = []
       if projects_array.length > 0
          projects_array.each do |repo|

             puts "\tFetching metadata for: #{repo}"

             begin
                # load repo metadata
                octokit_repo = client.repository(repo)
                project_title = octokit_repo.name
                project_owner = octokit_repo.owner.login
                project_description = octokit_repo.description
                project_url = "/#{REPO_DIR}/#{project_title}/"
                project_date = octokit_repo.updated_at

                # load contributor metadata
                octokit_contributors = client.contributors(repo)
                project_contributors = []
                for i in 0 ... [octokit_contributors.size, 10].min
                   contributor = octokit_contributors[i]
                   project_contributors << {
                      "login" => contributor.login,
                      "avatar" => contributor.rels[:avatar].href + "&s=50",
                      "url" => contributor.rels[:html].href
                   }
                end

                # load commit metadata
                octokit_commits = client.commits(repo)
                project_commits = []
                counter = 0
                for i in 0 ... octokit_commits.size
                   commit = octokit_commits[i]
                   commit_date = commit.commit.author.date
                   commit_message = commit.commit.message
                   commit_url = commit.rels[:html].href

                   commit_author_login = commit.author ? commit.author.login : ""
                   commit_author_url = (commit.author && commit.author.rels[:html]) ? commit.author.rels[:html].href : ""

                   project_commits << {
                      "date" => commit_date,
                      "message" => commit_message,
                      "url" => commit_url,
                      "author_login" => commit_author_login,
                      "author_url" => commit_author_url
                   }
                   counter += 1
                   break if counter == 5
                end

                readme_only = readmes_array.include?(repo)

                # assemble metadata
                project_data << {
                   "repo" => repo,
                   "title" => project_title,
                   "owner" => project_owner,
                   "description" => project_description,
                   "url" => project_url,
                   "contributors" => project_contributors,
                   "commits" => project_commits,
                   "readme_only" => readme_only
                }
             rescue Octokit::NotFound
                puts "\t\tERROR: Repository '#{repo}' not found on GitHub."
             rescue => e
                puts "\t\tAn unexpected error occurred for '#{repo}': #{e.message}"
             end
          end
       end

       # Sort by latest commit date
       project_data.sort! { |x, y| y["commits"].first["date"] <=> x["commits"].first["date"] rescue 0 }

       return project_data
    end

    def self.write_data(project_data, data_file)
       puts "4. Writing project data to #{data_file}"
       File.write(data_file, project_data.to_yaml)
    end
end

# --- Workflow Execution ---

def run_workflow(config_file)
    ReadmeDownloader.generate_readmes(config_file)
    MarkdownPreprocessor.process_markdown(config_file)
    project_data = DataGenerator.generate_data(config_file)
    DataGenerator.write_data(project_data, DATA_FILE)
    puts "\nWorkflow complete! Run 'jekyll serve' now."
end

# Check for GITHUB_TOKEN before running
if ENV['GITHUB_TOKEN'].nil? || ENV['GITHUB_TOKEN'].empty?
   puts "Warning: GITHUB_TOKEN environment variable is not set."
   puts "Metadata fetching (Step 3) may fail or be rate-limited."
end

run_workflow("_config.yml")