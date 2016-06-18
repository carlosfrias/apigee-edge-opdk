#!/usr/bin/env ruby

require 'getoptlong'

PLUGIN_NAME = 'tcpconns'

def usage
  puts("#{$0} -h <fqdn> [-i <sampling_interval>]")
  exit
end

# Main
begin
  # Sync stdout so that it will flush to collectd properly. 
  $stdout.sync = true

  # Parse command line options
  hostname = nil
  sampling_interval = 10  # sec, Default value
  opts = GetoptLong.new(
    [ '--hostid', '-h', GetoptLong::REQUIRED_ARGUMENT ],
    [ '--sampling-interval', '-i',  GetoptLong::OPTIONAL_ARGUMENT ]
  )
  opts.each do |opt, arg|
    case opt
      when '--hostid'
        hostname = arg
      when '--sampling-interval'
        sampling_interval = arg.to_i
    end
  end
  usage if !hostname

  # Collection loop
  while true do
    start_run = Time.now.to_i
    next_run = start_run + sampling_interval
    states = [
      'ESTAB',
      'SYN-SENT',
      'SYN-RECV',
      'FIN-WAIT-1',
      'FIN-WAIT-2',
      'TIME-WAIT',
      'UNCONN',
      'CLOSE-WAIT',
      'LAST-ACK',
      'LISTEN',
      'CLOSING',
    ]

   netdata = `/usr/sbin/ss state all -n 2>/dev/null`
   states.each do |state| 
    count = netdata.scan(/\s#{state}\s/).length 
    puts("PUTVAL #{hostname}/#{PLUGIN_NAME}/gauge-#{state} #{start_run}:#{count}")
   end
    
    # sleep to make the interval
    while((time_left = (next_run - Time.now.to_i)) > 0) do
      sleep(time_left)
    end
  end
end

