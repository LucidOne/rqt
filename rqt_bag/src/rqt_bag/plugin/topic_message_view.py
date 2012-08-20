# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from .message_view import MessageView


class TopicMessageView(MessageView):
    """
    A message view with a toolbar for navigating messages in a single topic.
    """
    #TODO implement toolbar portion of topic messageview
    def __init__(self, timeline, parent):
        MessageView.__init__(self, timeline)

        self._parent = parent
        self._topic = None
        self._stamp = None
        self._name = parent.objectName()
        self.parent.destroyed.connect(self._on_close)

    # 
    @property
    def parent(self):
        return self._parent

    @property
    def topic(self):
        return self._topic

    @property
    def stamp(self):
        return self._stamp

    # MessageView implementation

    def message_viewed(self, bag, msg_details):
        self._topic, _, self._stamp = msg_details[:3]

    # Events
    def _on_close(self):
        # TODO: needs to handle closing when a message hasn't been viewed yet
        if self._topic:
            self.timeline.popups.remove(self._name)
            self.timeline.remove_view(self._topic, self)

    def navigate_first(self):
        if not self.topic:
            return

        for entry in self.timeline.get_entries(self._topic, *self.timeline.play_region):
            self.timeline.playhead = entry.time
            break

    def navigate_previous(self):
        if not self.topic:
            return

        last_entry = None
        for entry in self.timeline.get_entries(self._topic, self.timeline.start_stamp, self.timeline.playhead):
            if entry.time < self.timeline.playhead:
                last_entry = entry

        if last_entry:
            self.timeline.playhead = last_entry.time

    def navigate_next(self):
        if not self.topic:
            return

        for entry in self.timeline.get_entries(self._topic, self.timeline.playhead, self.timeline.end_stamp):
            if entry.time > self.timeline.playhead:
                self.timeline.playhead = entry.time
                break

    def navigate_last(self):
        if not self.topic:
            return

        last_entry = None
        for entry in self.timeline.get_entries(self._topic, *self.timeline.play_region):
            last_entry = entry

        if last_entry:
            self.timeline.playhead = last_entry.time