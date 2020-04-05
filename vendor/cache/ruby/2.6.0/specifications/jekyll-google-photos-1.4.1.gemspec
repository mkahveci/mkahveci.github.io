# -*- encoding: utf-8 -*-
# stub: jekyll-google-photos 1.4.1 ruby lib

Gem::Specification.new do |s|
  s.name = "jekyll-google-photos".freeze
  s.version = "1.4.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Chirag Arora".freeze]
  s.date = "2020-03-16"
  s.description = "Embedd Google Photos Album to your Jekyll Site".freeze
  s.email = ["me@chia.ro".freeze]
  s.homepage = "https://github.com/heychirag/jekyll-google-photos".freeze
  s.licenses = ["MIT".freeze]
  s.rubygems_version = "3.1.2".freeze
  s.summary = "Embedd Google Photos Album to your Jekyll Site".freeze

  s.installed_by_version = "3.1.2" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4
  end

  if s.respond_to? :add_runtime_dependency then
    s.add_runtime_dependency(%q<jekyll>.freeze, ["~> 3.0"])
    s.add_development_dependency(%q<rake>.freeze, ["~> 11.0"])
    s.add_development_dependency(%q<rspec>.freeze, ["~> 3.5"])
    s.add_development_dependency(%q<rubocop>.freeze, ["~> 0.52"])
    s.add_development_dependency(%q<nokogiri>.freeze, ["~> 1.10"])
  else
    s.add_dependency(%q<jekyll>.freeze, ["~> 3.0"])
    s.add_dependency(%q<rake>.freeze, ["~> 11.0"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.5"])
    s.add_dependency(%q<rubocop>.freeze, ["~> 0.52"])
    s.add_dependency(%q<nokogiri>.freeze, ["~> 1.10"])
  end
end
