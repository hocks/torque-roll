#!/usr/bin/python
#
# A metric for Gschedule that publishes some PBS
# (Batch job launcher) metrics through Ganglia.
# For use with Rocks Clusters. 
#
# Output is similar to showq, with one metric per job
# in the queue.
#
# @Copyright@
# 
# 				Rocks
# 		         www.rocksclusters.org
# 		        version 4.2.1 (Cydonia)
# 
# Copyright (c) 2006 The Regents of the University of California. All
# rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks 
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: pbs.py,v $
# Revision 1.14  2007/08/31 08:44:25  royd
# Version updates for the upcoming 4.3.0 roll. Let's see how much trouble
# we run into this time...
#
# Revision 1.13  2006/09/11 22:50:00  mjk
# monkey face copyright
#
# Revision 1.12  2006/09/06 12:11:46  royd
# Fixed the nodespec parsing so it won't die every time someone submit
# a job containing out of the ordinary specs.
#
# Revision 1.11  2006/08/10 00:11:44  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/12 21:14:06  royd
# Added some new job states.
#
# Revision 1.9  2005/10/12 18:10:37  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/09/16 01:04:15  mjk
# updated copyright
#
# Revision 1.7  2005/08/31 19:49:59  bruno
# moved to the foundation
#
# included fix from Emir Imamagic
#
# Revision 1.6  2005/05/24 21:23:32  mjk
# update copyright, release is not any closer
#
# Revision 1.5  2004/11/02 00:57:05  fds
# Same channel/port as gmond. For bug 68.
#
# Revision 1.4  2004/04/13 20:55:36  fds
# Tweaks
#
# Revision 1.3  2004/04/13 03:12:26  fds
# Added full state names like SGE. Dont run as often now that we have update button on page.
#
# Revision 1.2  2004/04/11 21:38:15  fds
# Simpler, better tested.
#
# Revision 1.2  2003/11/17 18:55:24  fds
# Fixes from rockstar testing. Cluster top works again.
#
# Revision 1.1  2003/10/17 19:24:08  fds
# Presenting the greceptor daemon. Replaces gschedule and glisten.
#
# Revision 1.34  2003/08/27 23:10:55  mjk
# - copyright update
# - rocks-dist uses getArch() fix the i686 distro bug
# - ganglia-python spec file fixes (bad service start code)
# - found some 80col issues while reading code
# - WAN ks support starting
#
# Revision 1.33  2003/08/04 21:54:05  fds
# Encode nodelist with only hostname.
#
# Revision 1.32  2003/08/01 22:47:31  fds
# Small changes
#
# Revision 1.31  2003/04/15 20:32:12  fds
# Sometimes OpenPBS does not declare number of nodes in the expected way.
#
# Revision 1.30  2003/04/01 23:10:41  fds
# Added a well-defined entry point to metrics. The gmetric load-module code
# is much better now.
#
# New mpdring.py metric is an instance of KAgreement.
#
# Revision 1.29  2003/03/21 21:38:46  fds
# More responsive pbs reporting page. Less processing
# by the gschedule pbs.py module, which runs every 7 seconds.
# Simpler.
#
# Revision 1.28  2003/03/13 04:40:47  fds
# PyArg_ParseTupleAndKeywords() caused a memleak, even though I used as directed. Simpler parsing function seems to have cleaned things up. We are in the dark ages.
#
# Revision 1.27  2003/03/12 22:06:31  fds
# Running pbs monitor more often now that it is faster.
#
# Revision 1.26  2003/03/10 19:11:30  fds
# Converted to new Gmetric module.
#
# Revision 1.25  2003/02/25 22:57:26  fds
# Making the cleanup happed a bit quicker.
#
# Revision 1.24  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.23  2003/02/14 19:30:15  fds
# Correctly calculating number of processors/job for openPBS.
#
# Revision 1.22  2003/02/11 21:05:11  fds
# Works with OpenPBS
#
# Revision 1.21  2003/02/10 20:12:57  fds
# Now parsing qstat -f so fields are not truncated. Also collecting queued time so we can see how long our job has been sitting in the queue.
#
# Revision 1.20  2003/02/07 01:21:32  fds
# Checks to see qstat and pbsnodes are in our path.
#
# Revision 1.19  2003/02/05 00:19:02  fds
# Fixed from Stanford's Iceburg cluster.
#
# Revision 1.18  2003/02/04 21:51:50  fds
# Assuming cmds are in PATH. Not backwards compatible with 2.3.0.
#
# Revision 1.17  2003/01/24 20:53:05  fds
# More intelligent tmax value
#
# Revision 1.16  2003/01/24 20:25:29  fds
# Much simpler, using pbsnodes, fewer forks.
#
# Revision 1.15  2003/01/23 18:33:40  fds
# Encodes compute node names using the mpd-style encoder.
#
# Revision 1.14  2002/10/22 22:26:32  fds
# Now works when PBS is not around.
#
# Revision 1.13  2002/10/21 18:36:09  fds
# Gathering total processors count according to PBS.
#
# Revision 1.12  2002/10/18 21:33:25  mjk
# Rocks 2.3 Copyright
#
# Revision 1.11  2002/10/11 23:19:46  fds
# Doing the python daemon dance
#
# Revision 1.10  2002/10/11 19:26:41  fds
# Original design for PBS-Ganglia pages.
#
# Revision 1.9  2002/10/07 22:34:45  fds
# Testing on sandstorm, tmax() better.
#
# Revision 1.8  2002/10/07 17:38:52  fds
# Cleaner, simpler.
#
# Revision 1.7  2002/10/04 22:39:32  fds
# Specify a port
#
# Revision 1.6  2002/10/04 22:30:04  fds
# Activated metric timeout.
#
# Revision 1.5  2002/09/18 23:18:39  fds
# Changed the API so that accessor functions that are read-only don't have
# a 'get' prepended to their name. Allows us to easily specify port(), dmax(),
# tmax(), etc. PBS.py cleaned up significantly.
#
# Revision 1.4  2002/09/18 00:18:06  fds
# Debugging. Added devel options, such as alternative gmetric location.
#
# Revision 1.3  2002/09/12 23:02:07  fds
# Draft of pbs gsched module with new structure. Sends all metrics at once, which may potentially sum to quite a few of them.
#
# Revision 1.2  2002/09/12 18:50:22  mjk
# gmetric changes
#
#

import os
import time
from string import split,join,count,digits,strip
from gmon.Gmetric import publish
import gmon.events
# Our MPD-style name list encoder.
import gmon.encoder


class Job:
	pass


class PBS(gmon.events.Metric):
	"Monitors the PBS parallel batch queue using Ganglia."
	
	# How often we publish (in sec), on average.
	freq = 30

	# Information about each job. jobs[jobid]=pbsJob()
	jobs = {}
	# The number of processors PBS thinks are alive.
	totalP = 0

	state = { 'R': 'Running', 'Q': 'Queue Wait',
		'E': 'Exiting', 'H': 'Held', 'T': 'Transfering',
		'W': 'Waiting', 'C' : 'Completed', 'S' : 'Suspended'}

	def __init__(self, app):
		# Schedule every few seconds on average.
		gmon.events.Metric.__init__(self, app, self.freq)

		# Our enceventsoder to compact node name lists.
		self.e = gmon.encoder.Encoder("compute-%d-%d")


	def name(self):
		return "pbs"
		
		
	def schedule(self, sched):

		self.qstat = self.which("qstat")
		self.pbsnodes = self.which("pbsnodes")

		if self.qstat and self.pbsnodes:
			gmon.events.Metric.schedule(self, sched)
		else:
			self.info(
			"PBS: qstat, pbsnodes cmds are not in our path, exiting.")


	def findjobs(self):
		"Collect info in all jobs in queue."

		jobinfo=None

		for line in os.popen("%s -f" % (self.qstat)).readlines():

			# Assumes the qstat format will not change. (Obvious,
			# but critical).
			fields = map(strip, split(line[:-1], " = "))

			if not fields[0]: 
				continue

			if fields[0].count("Job Id:"):
				# This is a job line
				id = fields[0].split(': ')[1]

				jobid, queuehost = id.split('.',1)
				jobid = int(jobid)
		
				if jobid not in self.jobs:
					self.jobs[jobid] = Job()
				thisjob = self.jobs[jobid]

				thisjob.size = 1
				thisjob.queuehost = queuehost
				thisjob.nodes = []

			elif fields[0] == "Job_Name":
				thisjob.name = fields[1]

			elif fields[0] == "Job_Owner":
				thisjob.user = fields[1].split('@')[0]

			elif fields[0] == "job_state":
				thisjob.state = fields[1]

			# Find number of processors - different for OpenPBS and pbs.
			elif fields[0] == "Resource_List.nodes":
				procsum = 0
				for m in split(fields[1],"+"):
				    # each host entry can be as complex as
				    # (N|nodename):ppn=X:featureY:featureZ, but fortunately
				    # we only need to care about ints or ppn=X
				        nodes = 1
					ppn = 1
					nodespec = split(m,":")
					for n in nodespec:
					    if n.isdigit():
						nodes = int(n)
					    elif n.startswith("ppn="):
						_,ppn = n.split("=",1)
						ppn = int(ppn)
					procsum += nodes * ppn
				
				thisjob.size = procsum

			# Sometimes OpenPBS specifies jobsize with ncpus.
			elif fields[0] == "Resource_List.ncpus":
				thisjob.size = fields[1]
			
			# The job-state modification time. Used for both queued time
			# and running time. Time always in seconds.
			elif fields[0] == "mtime":
				t = time.strptime(fields[1],
							'%a %b %d %H:%M:%S %Y')
				t = t[:-1] + (time.daylight,)
				thisjob.mtime = time.mktime(t)

			# We need these two later to compute the remaining 
			# time for the job.
			elif fields[0] == "Resource_List.walltime":
				thisjob.walltime = fields[1]
			elif fields[0] == "resources_used.walltime":
				thisjob.used_time = fields[1]

	def getnodes(self):
		"Gathers details about a specific job"

		self.totalP=0

		for line in os.popen("%s -a" % (self.pbsnodes)).readlines():

			fields = map(strip, split(line[:-1], " = "))

			if not fields[0]: 
				continue
			
			if len(fields) == 1:
				# Take only host portion of name.
				node = split(fields[0],".")[0]
				continue

			if fields[0] == "state":
				state = fields[1]

			# Assumes "state" is before "np".
			elif fields[0] == "np" and \
				not count(state, "state-unknown"):
				self.totalP = self.totalP + int(fields[1])

			elif fields[0] == "jobs":
				ids = split(fields[1], ", ")
				for i in ids:
					cpu, id = split(i, "/")
					jobid = int(id.split('.')[0])
					if jobid in self.jobs:
						self.jobs[jobid].nodes.append(node)


	def port(self):
		# We may want to test on a development port.
		return 8649

	def dmax(self):
		# Delete these metrics in a few minutes unless refreshed.
		return self.freq * 3

	# Re-implemented from our superclass. Will publish many metrics at once.
	def run(self):
		"Publishes global and per-job PBS batch queue state."

		# Clean house.
		self.jobs={}

		# Get interesting PBS state.
		self.findjobs()
		
		# Find nodes associated with running jobs
		self.getnodes()

		# Publish current PBS global state.
		self.publish("queue-state", "P=%s" % (self.totalP), 
			dmax=self.dmax() * 4)

		# Publish all PBS jobs.
		for jobid in self.jobs.keys():
			Name = "queue-job-%s" % (jobid)

			info=self.jobs[jobid]

			# Delimit with ", " so it looks good, and we can
			# have spaces in the values.
			Value = "user=%s, P=%s, state=%s, started=%s" % \
				(info.user, info.size, self.state[info.state], 
				info.mtime)

			def remaining_time(total,used):
				th,tm,ts = map(int,total.split(":")
				uh,um,us = map(int,used.split(":")
				rt = (th*3600+tm*60+ts)-(uh*3600+um*60+us)
				rh, rest = divmod(rt,3600)
				rm, rs = divmod(rest,60)
				
			if info.state == "R":
				#rt = remaining_time(info.walltime,info.used_time)
				Value = Value + ", name=%s, nodes=%s" % \
					(info.name, self.e.encode(info.nodes))

			self.publish(Name, Value)

		# Whew! We're done. Make sure we are using ganglia-monitor-core
		# >= 2.5.1 with the cleanup thread to timeout stale pbs
		# metrics.


def initEvents():
	return PBS

