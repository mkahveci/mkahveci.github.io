# -*- encoding: utf-8 -*-
# stub: jekyll-pdf-embed 1.0.4 ruby lib

Gem::Specification.new do |s|
  s.name = "jekyll-pdf-embed".freeze
  s.version = "1.0.4"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Mihajlo Nesic".freeze]
  s.date = "2020-03-27"
  s.description = "\n\tJekyll PDF Embed is a ruby gem for Jekyll static site generator.\n\tIt allows user to easily embed external or local PDF files to any page or blog post.\n  ".freeze
  s.email = "nesicmihajlo98@gmail.com".freeze
  s.homepage = "https://github.com/MihajloNesic/jekyll-pdf-embed".freeze
  s.licenses = ["MIT".freeze]
  s.rubygems_version = "3.1.2".freeze
  s.summary = "Jekyll plugin for embedding PDF files to any page or post".freeze

  s.installed_by_version = "3.1.2" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4
  end

  if s.respond_to? :add_runtime_dependency then
    s.add_runtime_dependency(%q<jekyll>.freeze, [">= 0"])
  else
    s.add_dependency(%q<jekyll>.freeze, [">= 0"])
  end
end
