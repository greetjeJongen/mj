#!/usr/bin/env ruby
require 'optparse'
require 'net/http'
require 'json'

# Option parser
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: testr.rb [options]"

  opts.on("-f", "--file", "output to file") do |f|
    options[:file] = f
  end

  opts.on("-r", "--raw", "raw output") do |r|
    options[:raw] = r
  end
end.parse!

uri = URI('http://server.arne.tech:83/status/everyone')
response = Net::HTTP.get(uri)
r = JSON.parse(response)

max_length = 0
r.each do
  |student_info|
  if student_info['repoName'].length > max_length
    max_length = student_info['repoName'].length
  end
end
max_length += 1

result = ''
unless options[:raw]
  result += '%s' % 'repo'.ljust(max_length, ' ') + "│passed\n"
  result += '%s' % '────'.ljust(max_length, '─') + "├──────\n"
end

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

if options[:file]
  File.open("output.txt", "w+") {|f| f.write(result)}
else
  puts result
end