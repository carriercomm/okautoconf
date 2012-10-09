#!/usr/bin/perl
#
use strict;

my $debug = 1;

sub loggit {
	open L, '>>/var/log/asterisk/okautoconf.log';
	print L shift . "\n";
	close L;
}

# Extension called
my $ext = shift @ARGV;
# From which trunk to call
my $int = shift @ARGV;
 
loggit("okautoconfig, Got argv $ext, $int") if ($debug);
 
# Read the extension configuration file
open (E, "</etc/okautoconf/$ext") or
	exit(1);

# Get config line
my $cfg = <E>;
chomp($cfg);
my ($name, $callerid) = split('|', $cfg);

my @include = ();
foreach my $l (<E>) {
	chomp($l);
	push @include, $l;
}
 
loggit("okautoconfig, Paging " . join(', ', @include));

# Used for withing the asterisk extension config
print "SET VARIABLE CONFERENCEID \"$ext\"\n";

# Drop a call file into place
foreach my $number (@include) {
	open NMEGA, ">/var/spool/asterisk/tmp/okautoconf-$number";
	print NMEGA <<"	EOMEGA";
Channel: $int/$number
MaxRetries: 0
RetryTime: 60
WaitTime: 20
Context: custom-okautoconfmember
Extension: 1
Setvar: CONFERENCEID=$ext
Priority: 1
	EOMEGA
	close NMEGA;
	rename "/var/spool/asterisk/tmp/okautoconf-$number", "/var/spool/asterisk/outgoing/okautoconf-$number";
	loggit("okautoconf, Calling $number") if ($debug);
}


loggit("okautoconf, done") if ($debug);
 
exit 0;

