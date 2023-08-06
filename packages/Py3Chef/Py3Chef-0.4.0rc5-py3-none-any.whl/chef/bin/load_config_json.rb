#!/usr/bin/knife exec

##
# Dump a JSON representation of Chef client config
# Use configure third-party REST API clients, for example Py3Chef
# :D
##
require 'chef/workstation_config_loader'
require 'chef-config/path_helper'
require 'json'

# create a config loader.
# we point it at the "base chef config" for the host, as our fallback.
#
loader = ChefConfig::WorkstationConfigLoader.new '/etc/chef/client.rb', nil
#
# we tell chef that for this config loader, we'd like it to look
# for "dot d" style configs - ie. ~/.chef/config.d/ directory of config files -
# under the current user's home directory (~) and chef config directory (.chef).
#
ChefConfig::Config[:config_d_dir] = ChefConfig::PathHelper.home(".chef", "config.d")
#
# when the loader runs through, it'll look at the base layer config from the
# host, and overwrite with the config from ~/.chef/config.d/blah.rb if found.
# which is how you kinda expect config file hunting to go.
#
loader.load
# we can then dump the config as a pretty json blob for consuming downstream.
puts JSON.pretty_generate(Chef::Config.configuration)


## If you ever need to debug this app, uncomment the following line(s)
## Create breakpoint
# require 'pry'; binding.pry

## Inspect Chef::Application::Client instance
# client.inspect
#
## Inspect Chef::Config configuration state
# Chef::Config.configration

## Inspect other Chef::Config instance variables (state loaded by client.configure_chef)
# Chef::Config.instance_variables

## Inspect the knife executable to get a full picture by running `vim $(which knife)`
## $cat $(which knife)
#!/opt/chef/embedded/bin/ruby --disable-gems
#--APP_BUNDLER_BINSTUB_FORMAT_VERSION=1--
# ENV["GEM_HOME"] = ENV["GEM_PATH"] = nil unless ENV["APPBUNDLER_ALLOW_RVM"] == "true"
# require "rubygems"
# ::Gem.clear_paths

# <gem pins ommitted for brevity>
# gem "chef", "= 12.22.5"

# spec = Gem::Specification.find_by_name("chef", "= 12.22.5")
# bin_file = spec.bin_file("knife")
# Kernel.load(bin_file)
