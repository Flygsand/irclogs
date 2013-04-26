# -*- mode: ruby; tab-width: 2; indent-tabs-mode: nil -*-

require 'rubygems'
require 'bundler/setup'

require 'railsless-deploy'

load 'deploy' if respond_to?(:namespace)

set :application, "irclogs"

role :web, "#{application}.protomou.se"

set :scm, "git"
set :repository, "git@github.com:protomouse/#{application}.git"
set :branch, fetch(:branch, "master")
set :git_enable_submodules, 1

default_run_options[:pty] = true
ssh_options[:forward_agent] = true
set :use_sudo, false
set :user, "deploy"
set :deploy_via, :remote_cache
set :deploy_to, "/var/#{user}/apps/#{application}"

after "deploy:setup" do

  run "mkdir #{shared_path}/conf"

end

after "deploy:create_symlink" do 

  run "rm -rf #{current_path}/config.json"
  run "ln -s #{shared_path}/conf/config.json #{current_path}/config.json"

end

after "deploy:restart" do

  

end