--------------------------------
TORQUE ROLL DOCUMENTATION
--------------------------------

.. contents::


Introduction
================

The torque-roll provides a batch system for the Rocks_ Cluster Distribution.

.. _Rocks: http://www.rocksclusters.org

The batch system consists of the Torque resource manager and the Maui scheduler which together provides an alternative to the Sun Grid Engine (SGE) that comes as the default batch system with Rocks.  The torque roll will not work on a system that has an active sge-roll installed.  The best solution is to reinstall your frontend with the torque-roll instead of the sge-roll.

Roll basics
============

Included software.
--------------------

The torque roll contains software collected from the following places

============  =======================================================
Torque         http://www.clusterresources.com/products/torque
Maui           http://www.clusterresources.com/products/maui
mpiexec        http://www.osc.edu/~pw/mpiexec/
pbstools       http://www.osc.edu/~troy/pbs/
pbspython      ftp://ftp.sara.nl/pub/outgoing/
============  =======================================================



Where to get it
----------------

========================= ===================================================
Homepage (sadly outdated) http://uit.no/itavd/HPC-Rocks-PBS-Roll/
Download                  ftp://ftp.uit.no/pub/linux/rocks/torque-roll
Source code               http://devsrc.cc.uit.no/hg/torque/
========================= ===================================================

Installation
---------------

It is assumed that you know how to install a Rocks roll on a frontend, see the main Rocks documentation for an intro to installation of a Rocks cluster. You can either burn the roll iso on a CD or install from a central server, both methods are equivalent.

Building the roll from source
------------------------------

This is only relevant if you want to change something in how the torque-roll is built.  The default build should cover most needs.

Clone the repository into the rocks build tree on a frontend::

  cd /opt/rocks/share/devel/roll/src/
  hg clone http://devsrc.cc.uit.no/hg/torque/

Building is a three step process::

  cd torque/src/torque
  make rpm
  cd ../..
  rpm -i RPMS/x86_64/torque*.rpm
  make roll

You should now have a torque iso file that you can install on a frontend.

The torque rpm build depends on readline-devel and tclx-devel rpms being installed.


Using the torque-roll.
=======================

When the rocks frontend is installed with the torque-roll it will have a functioning batch system, but you will not be able to run any jobs until you have installed some compute nodes.  As you detect and install new compute nodes with ``insert-ethers`` they will automatically be included in the node list and start receiving jobs as soon as they are up and running.


Running jobs.
--------------

The normal way of using a batch system is through submitting jobs as scripts that get executed on the compute nodes.  A job script can be any shell (bash, csh, zsh), python, perl or whatever supports the # comment character.  The most normal is though to use sh or csh as job script syntax.  The job script is a regular script with some special comments that is meaningful to the batch system.  In torque all lines beginning with ``#PBS`` are interpreted by the batch system.  You submit the job with the ``qsub`` command::

  qsub runscript.sh


A simple run script.
---------------------

It is useful to give info about expected walltime and the number of cpus the job needs.  Here is how runscript.sh could look like::

  #!/bin/sh
  #PBS -lwalltime=1:00:00
  #PBS -lnodes=1
  
  ./do-my-work

This script asks for 1 hour runtime and will run on one cpu.  The job will terminate when the script exits or will be terminated by the batch system if it passes the 1 hour runtime limit.  The ``#PBS`` directives can also be given as commandline arguments to ``qsub`` like::

  qsub -lnodes=1,walltime=1:00:00 runscript.sh

Commandline arguments takes precedence over runscript directives.

A more advanced run script.
----------------------------------

Let us take a look at the following script, ``runscript2.sh``::

  #!/bin/sh
  #PBS -lwalltime=1:00:00
  #PBS -lnodes=10
  #PBS -lpmem=2gb
  #PBS -N parallel_simulation
  
  cd $PBS_O_WORKDIR

  mpirun ./do-my-work

``runscript2.sh`` is a parallel job that asks for 10 cpus and 2 gigabytes of memory per cpu, the scheduler will then make sure these resources are available to the job before it can start.  The runscript will be run on the first node in the nodelist assigned to this job and ``mpirun`` will take care of launching the parallel programme named ``do-my-work`` on all of the cpus assigned to this jobs, possibly on several compute nodes.  If you ask for more resources than is possibly available on a node the job will either be rejected at submit time or will never start.


Inspecting the jobs in the queue.
-----------------------------------

There are several commands that will give you detailed information about the jobs in the batch system.

==========  ====================  =========================================
Command      Task                   useful flags
==========  ====================  =========================================
showq        List jobs in queue     -r -- only running jobs
                                    -i -- only idle jobs
                                    -b -- only blocked jobs
                                    -u username -- only 
----------  --------------------  -----------------------------------------
qstat        List jobs in queue     -f jobid -- list details
                                    -n  -- list nodes assigned to job
==========  ====================  =========================================

While both showq and qstat do the same task the output is quite different::

  $ showq
  
  $ qstat


Scheduling features
======================

Maui provides a rich set of scheduling features.
-------------------------------------------------

Maui can schedule on cpus, walltime, memory, disk size, network topology and more...
We will focus on node distribution and how to make your users behave. 

Needed job info
-------------------

For scheduling to be useful one needs info about the jobs.
At least number of cpus and walltime. Memory requirements also useful.  For instance::

  #PBS -lwalltime=HH:MM:SS
  #PBS -lnodes=10:ppn=8
  #PBS -lpmem=1gb

Memory handling on linux
--------------------------

torque/maui supports two memory specification types, (p)mem and (p)vmem on linux.

* pmem is not enforced, used only as information to the scheduler.
* pvmem is enforced, terminating procs that cross the limit.
  limiting vmem size by setting ulimit -v on the processes

Torque hacking
-----------------

Torque is installed in /opt/torque. qmgr is the torque mgt. command

Friendly advice: backup your working config::

  # qmgr -c “print server” > /tmp/pbsconfig.txt

Roll back to escape from a messed up system::

  # qterm; pbs_server -t create
  # qmgr < /tmp/pbsconfig.txt

This will bring you back to where you started.  
*Remark:* this will wipe the whole queue setup and all currently queued and running jobs will be lost!

Maui hacking
--------------

Most things can be achieved by modifying /opt/maui/maui.cfg. 
Maui needs restart after changing the config file::

  service maui restart

*Advice:* If you can achieve the same thing by changing either torque or maui, use maui.
Restarting maui is rather lightweight operation, and seldom causes problems for live systems.
Restarting pbs_server can make the system oscillatory for a few minutes.
pbs_server needs to contact all pbs_moms to get back in state.


Prioritizing short jobs
-------------------------

Often it is useful to give shorter jobs higher priority.
Use the XFACTOR feature in maui rather than torque queues with different priorites.::

  XFACTORWEIGHT 1000

XFACTOR is defined as::

  XFACTOR=(walltime+queuetime)/walltime

XFACTOR will increase faster for shorter walltimes thus giving higher priorities for short jobs.
Depends on users giving reasonable walltime limits.


Prioritizing large jobs (maui)
----------------------------------

In a cluster with a diverse mix of jobs it is useful to prioritize the large jobs and make the smaller ones fill in the gaps.::

   CPUWEIGHT 1000
   MEMWEIGHT 100

This should be combined with fairshare to avoid starving users falling outside this prioritization.

Fairshare (maui)
-----------------

Also known as

   “Keeping all users equally unhappy”

Can be done on several levels
users, groups.....

Set a threshold::

  USERCFG[DEFAULT] FSTARGET=10
  FSWEIGHT 100

Users having used more than 10% will get reduced priority and vice versa.

Adjusting your policy
----------------------

You can play with the weights to fine-tune your scheduling policies::
  XFACTORWEIGHT 100
  FSWEIGHT 1000
  RESWEIGHT 10
  CPUWEIGHT 1000
  MEMWEIGHT 100

Analyze the prioritization with diagnose -p

Job node distribution
------------------------

Default is MINRESOURCE
Run on the nodes which gives the least unused resources.

Spread or pack?::

  NODEALLOCATIONPOLICY PRIORITY

Select the most busy nodes::

  NODECFG[DEFAULT] PRIORITYF=JOBCOUNT

Select the least busy nodes::

  NODECFG[DEFAULT] PRIORITYF=-1.0*JOBCOUNT

Node access policy
--------------------

Default access policy is SHARED
Can choose to limit this to SINGLEJOB or SINGLEUSER, for instance::

  NODEACCESSPOLICY SINGLEUSER

Single user access prevents users from stepping on each others toes while allowing good utilization for serial jobs.

Throttling policies
--------------------

Sometimes one needs to limit the user from taking over the system::

  MAXPROC, MAXPE, MAXPS, MAXJOB, MAXIJOB

All can be set for all or individual users and groups::

  USERCFG[DEFAULT], USERCFG[UserA] etc.

Debugging and analyzing
--------------------------

Lot of tools::

  pbsnodes 	-- node status
  qstat -f		-- all details of a job
  diagnose -n	-- node status from maui
  diagnose -p	-- job priority calculation
  showres -n	-- job reservation per node
  showstart	-- obvious
  checkjob/checknode – also pretty obvious..


Example: express queue
=======================

Goal: Supporting development and job script testing, but prevent misuse

Basic philosophy:

* Create a separate queue
* Give it the highest priority
* Throttle it so it is barely usable

Create the queue with qmgr::

  create queue express                     
  set queue express queue_type = Execution 
  set queue express resources_max.walltime = 08:00:00
  set queue express resources_default.nodes = 1:ppn=8
  set queue express resources_default.walltime = 08:00:00
  set queue express enabled = True                       
  set queue express started = True 

Increase the priority and limit the usage::

  CLASSWEIGHT             1000
  CLASSCFG[express] PRIORITY=1000 MAXIJOB=1  MAXJOBPERUSER=1 QLIST=express QDEF=express
  QOSCFG[express] FLAGS=IGNUSER

This will allow users to test job scripts and run interactive jobs with good turnaround
