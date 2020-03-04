#!/usr/bin/env ruby
require 'optparse'
require 'net/http'
require 'json'

# Option parser
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: testr.rb [options]"

  # f option, direct output to a file
  opts.on("-f", "--file", "output to file") do |f|
    options[:file] = f
  end

  # r option, print output without visual formatting (for easier data manipulation)
  opts.on("-r", "--raw", "raw output") do |r|
    options[:raw] = r
  end
end.parse!

# API call to DHT mainframe
uri = URI('http://server.arne.tech:83/status/everyone')
response = Net::HTTP.get(uri)
r = JSON.parse(response)

# Check which repo name is the longest
max_length = 0
r.each do
  |student_info|
  if student_info['repoName'].length > max_length
    max_length = student_info['repoName'].length
  end
end
max_length += 1

# Build output string
result = ''
unless options[:raw]
  result += '%s' % 'repo'.ljust(max_length, ' ') + "│passed\n"
  result += '%s' % '────'.ljust(max_length, '─') + "├──────\n"
end

# Build line for each repository
r.each do |student_info|
  result += '%s' % student_info['repoName'].ljust(max_length, ' ')
  passed_text = 'true'
  if student_info['passed'] == 0
    passed_text = 'false'
  end
  if options[:raw]
    result += "%s\n" % passed_text.ljust(2, ' ')
  else
    result += "│%s\n" % passed_text.ljust(2, ' ')
  end
end

# Output generation
if options[:file]
  File.open("output.txt", "w+") {|f| f.write(result)}
else
  puts result
end