#! /usr/bin/python
"""
Took from NLTK extensions made by the IXA-group: http://ixa.si.ehu.es/node/4470?language=en
"""
# -*- coding: utf-8 -*-
from nltk.tokenize.api import *


class EuskalToken(TokenizerI):

    def puntuakDesanbiguatu(self, tokens, index):
        # "."aren balio posibleak : 1. laburdura--> "(...)hala nola: kontrola-ezinezko berbalizazioa, desegituratutako sintaxia, etab."
        #			   2. "garren"--> "(...)1994. urtean(...)"
        #			   3. lerro amaiera--> "(...)esan zion.(...)
        #			   4. hiru puntu--> "(...)laukiak, hirukiak,... (...)

        exceptions = ['adib.', 'aip.', 'bibliog.', 'e.b.', 'etab.', 'e.a.', 'or.', 'orr.', 'ik.', 'lab.', 'pzta.',
                      'pta.', 'zenb.', 'zk.', 'zbko.', 'tel.', 'tf.', 'jn.', 'and.', 'año.', 'G.b.', 'esk.', 'ezk.',
                      'aptu.', 'sol.', 'eskra.', 'z.g.', 'k.', 'pl.', 'pas.', 'enp.', 'etorb.', 'ibde.', 'zum.',
                      'prob.', 'P.-B.', 'P.-K.', 'P.-Ku.', 'P.D.', 'izpta.', 'stua.', 'sin.', 'ztua.', 'or.', 'p.m.',
                      'a.m.', 'K.a.', 'K.o.', 'al.', 'as.', 'az.', 'og.', 'or.', 'lr.', 'ig.']
        actual = tokens[index]
        previous = None
        next = None
        if index > 0:  # testuko lehengo tokena --> ez du aurreko tokenik!
            previous = tokens[index - 1]
        if index < len(tokens) - 1:  # testuko azken tokena --> ez du hurrengo tokenik!
            next = tokens[index + 1]
        tokenLength = len(actual.split('.'))

        if tokenLength > 1:  # tokenak puntua du
            if tokenLength == 2:  ##puntu bakarra dago
                # kasu oso berezi bat: '.)' edo antzekoak:mota=0-> puntua eta gero ez dago ezer!
                # mota=1-> puntua eta gero zerbait dago
                count = actual.count('')
                if count == 1:
                    mota = 0
                else:
                    mota = 1
                if mota == 0:  # azken sinboloa puntua da
                    helper = actual.split('.')[0]
                    if not helper.isdigit():
                        # kasu honetan zera aztertu behar da: laburdura ala lerro amaiera.
                        if next != None:
                            if next[0].isupper():
                                # bi aukera: laburdura ala puntu arrunta
                                if actual in exceptions:  # laburdura
                                    actual = [actual]
                                else:  # puntu arrunta
                                    actual = [actual.split('.')[0]]
                                    actual.append('.')
                            # else : Laburdura bat izango da eta bere horretan utziko da
                            else:
                                actual = [actual]
                        else:
                            if actual in exceptions:
                                actual = [actual]
                            else:  # puntu arrunta
                                actual = [actual.split('.')[0]]
                                actual.append('.')
                    else:  # zenbakia da:1984.
                        actual = [actual]

                else:  # puntua eta gero zerbait dago: 1.984 edota '.)' bezalako egiturak /////LO PRIMERO exceptions tratatu!!!
                    helper = actual.split('.')
                    if helper[0].isdigit():  # 1.984 formatua
                        actual = [actual]
                    else:  # '.)' formatua
                        actual = [helper[0]]
                        actual.append('.')
                        actual.append(helper[1])
        # else: 3 puntua eta puntu bat baino gehiagoko zenbakiak!!!!

        ###############33paluego
        # if tokenLength == 4: # (...)--> hiru puntuen agerpena
        # actual=[actual.split('...')[0]]
        # actual.append('...')
        # else: # zenbakia bada bere horretan utzi--> "1984. urtean..." egiturakoa da // 1.984 ere onartzen da
        #	actual=[actual]
        # else:Ez du punturik
        else:
            actual = [actual]
        return actual

    def puntuKomaIkurrak(self, token):
        if token == ';':
            tokens = token
        else:
            tokens = token.split(';')
        if len(tokens) > 1:
            helper = [tokens[0]]
            helper.append(';')
            tokens = helper
        return tokens

    def biPuntuIkurrak(self, token):
        if token == ':':
            tokens = token
        else:
            tokens = token.split(':')
        if len(tokens) > 1:
            helper = [tokens[0]]
            helper.append(':')
            tokens = helper
        return tokens

    def komaIkurrak(self, token):
        if token == ',':
            tokens = token
        else:
            tokens = token.split(',')
        if len(tokens) > 1:
            helper = [tokens[0]]
            helper.append(',')
            tokens = helper
        return tokens

    def galderaIkurrak(self, token):
        if token == '?':
            tokens = token
        else:
            tokens = token.split('?')
        if len(tokens) > 1:
            helper = [tokens[0]]
            helper.append('?')
            tokens = helper
        return tokens

    def harriduraIkurrak(self, token):
        if token == '!':
            tokens = token
        else:
            tokens = token.split('!')
        if len(tokens) > 1:
            helper = [tokens[0]]
            helper.append('!')
            tokens = helper
        return tokens

    def parentesiaIrekiIkurrak(self, token):
        if token == '(':
            tokens = token
        else:
            tokens = token.split('(')
        if len(tokens) > 1:
            helper = ['(']
            helper.append(tokens[1])
            tokens = helper
        return tokens

    def parentesiaItxiIkurrak(self, token):
        if token == ")":
            tokens = [token]
        else:
            tokens = token.split(')')
        if len(tokens) > 1:
            helper = [tokens[0]]
            helper.append(')')
            tokens = helper
        return tokens

    def komatxoakIkurrak(self, token):
        if token == '"':
            tokens = token
        else:
            tokens = token.split('"')
        if len(tokens) > 1:
            # erabaki hasierakoak ala bukaerakoak diren:
            if tokens[0] == '':
                helper = ['"']
                helper.append(tokens[1])
                tokens = helper
            else:
                helper = [tokens[0]]
                helper.append('"')
                tokens = helper
        return tokens

    def komatxoBakunakIkurrak(self, token):
        if token == "'":
            tokens = token
        else:
            tokens = token.split("'")
        if len(tokens) > 1:
            if tokens[0] == '':
                helper = ["'"]
                helper.append(tokens[1])
                tokens = helper
            else:
                helper = [tokens[0]]
                helper.append("'")
                tokens = helper
        return tokens

    def tokenize(self, s):
        whiteS = s.split()
        ema = []
        ema1 = []
        ema2 = []
        ema3 = []
        ema4 = []
        ema5 = []
        ema6 = []
        ema7 = []
        ema8 = []
        ema9 = []
        for index in range(0, len(whiteS)):
            ema.extend(self.puntuakDesanbiguatu(whiteS, index))
        for index in range(0, len(ema)):
            lag = ema[:]
            ema1.extend(self.puntuKomaIkurrak(lag[index]))
        for index in range(0, len(ema1)):
            lag = ema1
            ema2.extend(self.biPuntuIkurrak(lag[index]))
        for index in range(0, len(ema2)):
            lag = ema2
            ema3.extend(self.komaIkurrak(lag[index]))
        for index in range(0, len(ema3)):
            lag = ema3
            ema4.extend(self.galderaIkurrak(lag[index]))
        for index in range(0, len(ema4)):
            lag = ema4
            ema5.extend(self.harriduraIkurrak(lag[index]))
        for index in range(0, len(ema5)):
            lag = ema5
            ema6.extend(self.parentesiaIrekiIkurrak(lag[index]))
        for index in range(0, len(ema6)):
            lag = ema6
            ema7.extend(self.parentesiaItxiIkurrak(lag[index]))
        for index in range(0, len(ema7)):
            lag = ema7
            ema8.extend(self.komatxoakIkurrak(lag[index]))
        for index in range(0, len(ema8)):
            lag = ema8
            ema9.extend(self.komatxoBakunakIkurrak(lag[index]))

        return ema9

###############################################################################