# -*- coding: utf-8 -*-

__author__ = 'Flurin Rindisbacher'

import unittest
import os
from .. import speech_recognition
from ..exceptions import RecognitionException, CommunicationException

def server_response_stub(success_answer=True,response_text=''):
    class ServerResponse(object):
        def __init__(self, a, t):
            self.ok = a
            self.text = t
    def send_request(url, data, headers):
        return ServerResponse(success_answer, response_text)

    return send_request

class TestGoogleSpeechRecognition(unittest.TestCase):
    def setUp(self):
        # set up some possible API server response
        # request was unsuccessful
        self.no_server_response = server_response_stub(False)
        # server did response, but could not recognize the data
        self.no_recognition = server_response_stub(True, '{"status":0,"id":"7eea7cfb6a09168431e8d76b10842947-1","hypotheses":[]}\n')
        # server successfully recognized "just an example"
        self.recognition_success = server_response_stub(True, u'{"status":0,"id":"7eea7cfb6a09168431e8d76b10842947-1","hypotheses":[{"utterance":"just an example","confidence":0.9}]}\n')
        self.input_flac = os.path.dirname(os.path.realpath(__file__)) + '/files/1.flac'

    def test_recognize_success(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.recognition_success
        result = cls.recognize(self.input_flac, format='flac')
        self.assertEqual(result['text'], 'just an example')

    def test_recognize_failure(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.no_recognition
        self.assertRaises(RecognitionException, cls.recognize, self.input_flac, 'flac')

    def test_recognize_no_server_response(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.no_server_response
        self.assertRaises(CommunicationException, cls.recognize, self.input_flac, 'flac')   

    def test_send_request(self):
        pass

    def test_conversion(self):
        pass
