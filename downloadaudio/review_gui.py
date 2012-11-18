#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


"""
Present files and let the user decide what to do with them.

Show a list of downoladed files and present the user with a few
choices what to do wit each:
* Save: Put on the card and store the file. This is the ideal case.
# Possible addition: * Keep file: Keep the file on disk but don't put
 it on the card.
* Delete: Just discard the file.

* Blacklist: Discard the file and also add the hash to a list of files
             that wil lbe automatically discarded in the future.
"""

import os

from PyQt4.QtGui import QButtonGroup, QDialog, QDialogButtonBox, QGridLayout, \
    QIcon, QLabel, QPixmap, QPushButton
from PyQt4.QtCore import SIGNAL, SLOT

from aqt import mw
from anki.lang import _
from anki.sound import play, playFromText

from blacklist import add_black_hash


icons_dir = os.path.join(mw.pm.addonFolder(), 'downloadaudio', 'icons')

# to make the code a bit more readable
action = {'add': 0, 'keep': 1, 'delete': 2, 'blacklist': 3}


def store_or_blacklist(note, retrieved_data):
    if not note or not retrieved_data:
        raise ValueError('Nothing downloaded')
    review_files = ReviewFiles(note, retrieved_data)
    if not review_files.exec_():
        remove_all_files(retrieved_data)
        raise RuntimeError('User cancel')
    # Go through the list once and just do what needs to be done.
    # Keep track if we have to do some clean up.
    items_added = False
    for idx, (source, dest, text, dl_fname, dl_hash, extras, icon) \
            in enumerate(retrieved_data):
        action_id = review_files.buttons_groups[idx].checkedId()
        if action_id == action['add']:
            items_added = True
            note[dest] += '[sound:' + dl_fname + ']'
        if action_id == action['delete']:
            os.remove(os.path.join(mw.col.media.dir(), dl_fname))
        if action_id == action['blacklist']:
            add_black_hash(dl_hash)
    if items_added:
        note.flush()
        # We have to do different things here, for download during
        # review, we should reload the card and replay. When we are in
        # the add dialog, we do a field update there.
        rnote = None
        try:
            rnote = mw.reviewer.card.note()
        except:
            # Could not get the note of the reviewer's card. Probably
            # not reviewing at all.
            return
        if note == rnote:
            # The note we have is the one we were reviewing, so,
            # reload and replay
            mw.reviewer.card.load()
            mw.reviewer.replayAudio()


def remove_all_files(files_etc):
    for source, dest, text, dl_fname, dl_hash, extras, icon\
            in files_etc:
        os.remove(os.path.join(mw.col.media.dir(), dl_fname))


class ReviewFiles(QDialog):
    """
    A Dialog to let the user keep or discard files.
    """

    def __init__(self, note, files_list):
        self.note = note
        self.list = files_list
        super(ReviewFiles, self).__init__()  # Cut-and-pasted
        self.buttons_groups = []
        self.text_help = _(u"""<h4>Text used to retrieve audio.</h4>
<p>Mouse over the texts below to see further information.</p>""")
        self.play_help = u"<h4>Play the retrieved file.</h4>"
        self.play_old_help = _(u"""<h4>Play the current content of the
 audio field.</h4>
<p>No button means the field is empty. Hovering over the button shows
the current field content as text.</p> """)
        self.play_old_empty_line_help = _(u"The target field is empty.")
        self.add_help_text_long = _(u"""<h4>Add the sound to the card.</h4>
<p>This is the normal thing to select for a good download.
(You may want to select only one file in this column.)</p>""")
        self.add_help_text_short = _(u"Add this sound to the card")
        self.keep_help_text_long = _(u"""<h4>Keep the file.</h4>
<p>Keep this file in the media collection folder, but don’t add it to
the card. (This means the file will show up as an unused medium and
may be deleted during the unused media check.</p>""")
        self.keep_help_text_short = _(u"Keep this file")
        self.delete_help_text_long = _(u"""<h4>Delete the file.</h4>
<p>This is the normal thing to do with a file you don’t like.</p>""")
        self.delete_help_text_short = _(u"Delete this file")
        self.blacklist_help_text_long = _(u"""<h4>Blacklist the file.</h4>
Add an idetifier for this file to a blacklist. When this file is
downloaded again, it will be silently dropped. This behaviour is
useful for Japanesepod downloads. When your downloaded file tells you
that they are sorry, will add this soon &c., click on this.""")
        self.blacklist_help_text_short = _(u"Blacklist this file")
        self.initUI()

    def initUI(self):
        self.setWindowTitle(_(u'Anki – Download audio'))
        self.setWindowIcon(QIcon(":/icons/anki.png"))
        layout = QGridLayout()
        self.setLayout(layout)
        explanation = QLabel(self)
        if len(self.list) > 1:
            explanation.setText(
                _(u'Please select an action for each downloaded file:'))
        else:
            explanation.setText(_(u'Please select what to do with the file:'))
        layout.addWidget(explanation, 0, 0, 1, 8)
        text_head_label = QLabel(_(u'<b>Source text</b>'), self)
        text_head_label.setToolTip(self.text_help)
        layout.addWidget(text_head_label, 1, 0, 1, 2)
        play_head_label = QLabel(_(u'play'), self)
        play_head_label.setToolTip(self.play_help)
        layout.addWidget(play_head_label, 1, 2)
        play_old_head_label = QLabel(_(u'play old'), self)
        play_old_head_label.setToolTip(self.play_old_help)
        layout.addWidget(play_old_head_label, 1, 3)
        add_head_label = QLabel(_(u'add'), self)
        add_head_label.setToolTip(self.add_help_text_long)
        layout.addWidget(add_head_label, 1, 4)
        keep_head_label = QLabel(_(u'keep'), self)
        keep_head_label.setToolTip(self.keep_help_text_long)
        layout.addWidget(keep_head_label, 1, 5)
        delete_head_label = QLabel(_(u'delete'), self)
        delete_head_label.setToolTip(self.delete_help_text_long)
        layout.addWidget(delete_head_label, 1, 6)
        blacklist_head_label = QLabel(_(u'blacklist'), self)
        blacklist_head_label.setToolTip(self.blacklist_help_text_long)
        layout.addWidget(blacklist_head_label, 1, 7)
        rule_label = QLabel('<hr>')
        layout.addWidget(rule_label, 2, 0, 1, 8)
        self.create_rows(layout)
        dialog_buttons = QDialogButtonBox(self)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        self.connect(dialog_buttons, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(dialog_buttons, SIGNAL("rejected()"),
                     self, SLOT("reject()"))
        layout.addWidget(dialog_buttons, len(self.buttons_groups) + 3, 0, 1, 8)

    def create_rows(self, layout):
        play_button_group = QButtonGroup(self)
        old_play_button_group = QButtonGroup(self)
        for num, (source, dest, text, dl_fname, dl_hash, extras, icon)\
                in enumerate(self.list, 3):
            ico_label = QLabel('', self)
            if icon:
                # Two changes to the old version: We pass around a
                # QImage, not a QPixmap (because we can *have* a
                # QImage for the the standalone downloader) and we
                # should handle the case that we have a None object
                # here. (Also, we don't scale up 16x16 images.)
                ico_label.setPixmap(QPixmap.fromImage(icon))
            layout.addWidget(ico_label, num, 0)
            tt_label = QLabel(text, self)
            tt_label.setToolTip(
                self.build_text_help_label(text, source, extras))
            layout.addWidget(tt_label, num, 1)
            # Play button.
            t_play_button = QPushButton(self)
            play_button_group.addButton(t_play_button, num - 3)
            t_play_button.setToolTip(self.play_help)
            t_play_button.setIcon(QIcon(os.path.join(icons_dir, 'play.png')))
            layout.addWidget(t_play_button, num, 2)
            if self.note[dest]:
                t_play_old_button = QPushButton(self)
                old_play_button_group.addButton(t_play_old_button, num - 3)
                t_play_old_button.setIcon(
                    QIcon(os.path.join(icons_dir, 'play.png')))
                t_play_old_button.setToolTip(self.note[dest])
                layout.addWidget(t_play_old_button, num, 3)
            else:
                dummy_label = QLabel('', self)
                dummy_label.setToolTip(self.play_old_empty_line_help)
                layout.addWidget(dummy_label, num, 3)
            # The group where we later look what to do:
            t_button_group = QButtonGroup(self)
            t_button_group.setExclusive(True)
            # Now the four buttons
            t_add_button = QPushButton(self)
            t_add_button.setCheckable(True)
            t_add_button.setChecked(True)
            t_add_button.setFlat(True)
            t_add_button.setToolTip(self.add_help_text_short)
            t_add_button.setIcon(QIcon(os.path.join(icons_dir, 'add.png')))
            layout.addWidget(t_add_button, num, 4)
            t_button_group.addButton(t_add_button, action['add'])
            t_keep_button = QPushButton(self)
            t_keep_button.setCheckable(True)
            t_keep_button.setFlat(True)
            t_keep_button.setToolTip(self.keep_help_text_short)
            t_keep_button.setIcon(QIcon(os.path.join(icons_dir, 'keep.png')))
            layout.addWidget(t_keep_button, num, 5)
            t_button_group.addButton(t_keep_button,  action['keep'])
            t_delete_button = QPushButton(self)
            t_delete_button.setCheckable(True)
            t_delete_button.setFlat(True)
            t_delete_button.setToolTip(self.delete_help_text_short)
            t_delete_button.setIcon(QIcon(os.path.join(icons_dir,
                                                       'delete.png')))
            layout.addWidget(t_delete_button, num, 6)
            t_button_group.addButton(t_delete_button,  action['delete'])
            t_blacklist_button = QPushButton(self)
            t_blacklist_button.setCheckable(True)
            t_blacklist_button.setFlat(True)
            t_blacklist_button.setToolTip(self.blacklist_help_text_short)
            t_blacklist_button.setIcon(QIcon(os.path.join(icons_dir,
                                                          'blacklist.png')))
            layout.addWidget(t_blacklist_button, num, 7)
            t_button_group.addButton(t_blacklist_button,  action['blacklist'])
            self.buttons_groups.append(t_button_group)
        play_button_group.buttonClicked.connect(
            lambda button: play(self.list[play_button_group.id(button)][3]))
        old_play_button_group.buttonClicked.connect(
            lambda button: playFromText(
                self.note[self.list[old_play_button_group.id(button)][1]]))

    def build_text_help_label(self, text, source, extras):
        ret_text = _(u'Source text: <b>{0}</b><br>From field: {1}')\
            .format(text, source)
        for key, value in extras.items():
            ret_text += u'<br>{0}: {1}'.format(key, value)
        return ret_text
