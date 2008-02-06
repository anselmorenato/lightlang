# XSL - graphical interface for SL
# Copyright (C) 2007-2016 Devaev Maxim
#
# This file is part of XSL.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from PyQt4 import Qt
import Const
import Config

#####
GoogleTranslateHost = "translate.google.com"

#####
class GoogleTranslate(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		self.http = Qt.QHttp()
		self.http_output = Qt.QByteArray()

		#####

		self.connect(self.http, Qt.SIGNAL("stateChanged(int)"), self.setStatus)
		self.connect(self.http, Qt.SIGNAL("readyRead(const QHttpResponseHeader &)"), self.setText)


	### Public ###

	def translate(self, langpair, text) :
		self.http.clearPendingRequests()
		self.http_output.clear()

		self.clearRequestSignal()
		self.wordChangedSignal(self.tr("Google Translate"))
		self.textChangedSignal(self.tr("Please wait..."))

		text = Qt.QString.fromLocal8Bit(str(Qt.QUrl.toPercentEncoding(text)))

		http_request_header = Qt.QHttpRequestHeader("GET",
			"/translate_t?langpair="+langpair+"&text="+text)
		http_request_header.setValue("Host", GoogleTranslateHost)
		http_request_header.setValue("User-Agent", "Mozilla/5.0")

		self.http.setHost(GoogleTranslateHost)
		self.http.request(http_request_header)
		self.http.close()


	### Private ###

	def setStatus(self, state) :
		if state == Qt.QHttp.Unconnected :
			self.statusChangedSignal(Qt.QString())
		elif state == Qt.QHttp.HostLookup :
			self.statusChangedSignal(self.tr("Looking up host..."))
		elif state == Qt.QHttp.Connecting :
			self.statusChangedSignal(self.tr("Connecting..."))
		elif state == Qt.QHttp.Sending :
			self.statusChangedSignal(self.tr("Sending request..."))
		elif state == Qt.QHttp.Reading :
			self.statusChangedSignal(self.tr("Reading data..."))
		elif state == Qt.QHttp.Connected :
			self.statusChangedSignal(self.tr("Connected"))
		elif state == Qt.QHttp.Closing :
			self.statusChangedSignal(self.tr("Closing connection..."))

	def setText(self) :
		self.http_output.append(self.http.readAll())

		codec = Qt.QTextCodec.codecForName("UTF-8")
		text = codec.toUnicode(self.http_output.data())

		# FIXME: string hack
		index = text.indexOf("<div id=result_box dir=")
		text = text[index:]
		index = text.indexOf("</div>")
		text = text[29:index]

		self.textChangedSignal(text)


	### Signals ###

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def statusChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), text)