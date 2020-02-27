#!/usr/bin/env ruby
require 'optparse'
require 'net/http'

# Option parser
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: testr.rb [options]"

  opts.on("-a", "--all_results", "Get all student results") do |a|
    options[:all] = a
  end

  opts.on("-f", "--file", "Put output in file") do |f|
    options[:file] = f
  end
end.parse!

p options.all?

response = Net::HTTP.get('http://server.arne.tech', '/')
#response_body = response.body
response_body = response

if options.all?
  File.open("output.txt", "a+") {|f| f.write(response_body) }
end

