#
# $Id: Makefile,v 1.9 2006/09/11 22:50:00 mjk Exp $
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
# $Log: Makefile,v $
# Revision 1.9  2006/09/11 22:50:00  mjk
# monkey face copyright
#
# Revision 1.8  2006/09/07 07:53:43  royd
# updates for 3.2.6p16
#
# Revision 1.7  2006/08/10 00:11:44  mjk
# 4.2 copyright
#
# Revision 1.6  2005/10/12 18:10:38  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:04:15  mjk
# updated copyright
#
# Revision 1.4  2005/05/24 21:23:33  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/01/27 08:48:20  royd
# Small mods due to changes in the tar structure in maui 3.2.6p11
#
# Revision 1.2  2003/10/29 23:13:16  mjk
# roll builds
#
# Revision 1.1  2003/10/29 18:15:27  mjk
# start pbs roll
#
# Revision 1.15  2003/01/24 19:14:17  bruno
# added licensing files
#
# Revision 1.14  2003/01/16 22:11:36  bruno
# added new version -- 3.2.5p2
#
# Revision 1.13  2003/01/16 15:49:04  bruno
# new release of maui
#
#

REDHAT.ROOT = $(PWD)/../../

ROCKSROOT = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

include version.mk

SEDSPEC = \
        -e 's%@NAME@%$(NAME)%g' \
        -e 's%@VERSION@%$(VERSION)%g' \
        -e 's%@RELEASE@%$(RELEASE)%g' \
        -e 's%@VENDOR@%$(VENDOR)%g' \
        -e 's%@COPYRIGHT@%$(COPYRIGHT)%g' \
        -e 's%@VAR@%$(REDHAT.VAR)%g' \
        -e 's%@PATCH@%$(PATCH)%g'


pretar::
	cp maui-3.2.6p19-correct-sprintf.patch $(REDHAT.SOURCES)
	cp maui-$(VERSION)$(PATCH)$(SNAPSHOT).tar.gz $(REDHAT.SOURCES)/maui-$(VERSION)$(PATCH).tar.gz


clean::
	rm -rf maui-$(VERSION).$(RELEASE)
