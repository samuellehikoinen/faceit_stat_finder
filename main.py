#!/usr/bin/env python3
import sys
import requests
import os
import random
import string
import json
from time import sleep


def hae_tiedot():
#Funktio hakee tiedot siinä olevan käyttäjän syötteen perusteella
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }

    print("Syötä 'status' komennon vastaus tähän: ")
    
    #try-except lausekkeessa haetaan käyttäjän syöte
    try:
        lopullinen = []
        while True:
            syote = input()
            if syote == "exit": #jos syöte = exit, suljetaan ikkuna
                sys.exit()
            if syote == "ohjeet": #jos syöte = ohjeet, avataan ohjeikkuna
                ohje()
            if not syote: break
            else:
                lopullinen.append(syote)
    #jos käyttäjä sulkee ikkunan manuaalisesti esim. näppäinoikotiellä
    except KeyboardInterrupt:
        print("Ohjelma keskeytyi manuaalisesti käyttäjän toimesta")
        return

    #syote oletettavasti muotoa:
    # 3 2 "Samua" STEAM_0:0:47889092 04:20 69 0 active 420420
    # 6 5 "Jole" STEAM_1:0:435021706 04:20 69 0 active 133769

    rivi = 0
    #käydään syöte läpi rivi kerrallaan
    try:
        while rivi < len(lopullinen):
            if(lopullinen[rivi].find('STEAM_') != -1):
                steamid = hae_id(lopullinen[rivi])
                if steamid != "":
                    url = 'https://steamidfinder.com/lookup/' + steamid
                    vastaus = requests.post(url, headers=headers)
                    etsi_kayttaja(headers, vastaus)
                    print()

                    del lopullinen[rivi]
                    #ei koroteta rivin indeksiä, jos rivi poistetaan
                else:
                    rivi+=1
            else:
                rivi+=1
    except:
        print("Ei saada yhteyttä palvelimeen.")


def hae_id(rivi):
#Funktio palauttaa steamID:n
    try:
        steamid = rivi[int(rivi.index('STEAM_')):rivi.index(' ',int(rivi.index('STEAM_')))]
        return steamid
    except:
        print("Virheellinen syöte!"+"\n")
        return ""


def etsi_kayttaja(headers, vastaus):
#Hakee pelaajan id:n 
    vastaus = vastaus.text
    if(vastaus.find('friends=') != -1):
        kayttaja = vastaus[int(vastaus.index('friends='))+8:int(vastaus.index('friends='))+25]
        
        url2 = 'https://faceitfinder.com/profile/' + kayttaja
        vastaus2 = requests.post(url2, headers=headers)
        tulosta_tiedot(vastaus2)
    else:
        print("Käyttäjää ei löytynyt!")


def tulosta_tiedot(tiedot):
#tulostaa haetun käyttäjän matsit, elon, K/D:n ja voittoprosentin
    tt = tiedot.text
    
    #tarkistetaan onko käyttäjän steamID syöte virheellinen
    try:
        nimi = tt[int(tt.index('<span>'))+6:tt.index('<',int(tt.index('<span>')+6))]
    except:
        print("Käyttäjää ei löytynyt!")
        return
    
    #tarkistetaan löytyykö käyttäjän tiedot faceitin tietokannasta
    try:
        #haetaan palvelimen palauttamasta tekstistä halutut tiedot
        elo = tt[int(tt.index('ELO:'))+13:tt.index('<',int(tt.index('ELO:')+13))]
        matsit = tt[int(tt.index('Matches:'))+17:tt.index('<',int(tt.index('Matches:')+17))]
        voittoprosentti = tt[int(tt.index('Winrt:'))+15:tt.index('<',int(tt.index('Winrt:')+15))]
        kd = tt[int(tt.index('K/D:'))+13:tt.index('<',int(tt.index('K/D:')+13))]
        hs = tt[int(tt.index('HS: <strong>'))+12:tt.index('<',int(tt.index('HS: <strong>')+12))]
        
        level = 1
        if(int(elo) >  800): level = 2
        if(int(elo) >  950): level = 3
        if(int(elo) > 1100): level = 4
        if(int(elo) > 1250): level = 5
        if(int(elo) > 1400): level = 6
        if(int(elo) > 1550): level = 7
        if(int(elo) > 1700): level = 8
        if(int(elo) > 1850): level = 9
        if(int(elo) > 2000): level = 10

        print("Nimi: " + nimi)
        print("ELO: " + elo + "\t(taso: " + str(level)+")")
        print("Matsit: " + matsit + "\t(voitot: " + voittoprosentti + ")")
        print("K/D: " + kd + "\t(HS: " + hs + ")")
    except:
        print("Käyttäjää "+nimi+" ei löytynyt Faceitista!")
    return


def ohje():
#Funktio tulostaa käyttöohjeet
    print("===============OHJEET===============")
    print("Ohjelma tulostaa CS:GO ottelun pelaajien Faceit tiedot")
    print("Kirjoita CS:GO pelissä konsoliin 'status'")
    print("ja kopioi vastaus syöte kenttään")
    print("Suorittamalla rivinvaihdon kahdesti ohjelma alkaa hakea tietoja")
    print("Komennolla 'exit' ohjelma sulkeutuu")


#Silmukka pitää komentoikkunaa auki, kunnes aliohjelman päästä se suljetaan
if __name__ == '__main__':
    print("===CS:GO match players Faceit stats===\nv1.2.5\n©Samuel Lehikoinen 2021\n")
    print("Ohjelman käyttöohjeet aukeavat komennolla 'ohjeet'")
    while True:
        hae_tiedot()
