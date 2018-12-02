import json
import requests
import re
import time
from pprint import pprint

MAX_MANA_COST = 12
MAX_TEXT_LENGTH = 100
TEXT_DIV = 5

class Card:
  def __init__(self, name):
    self.name = name
    self.flying = False
    self.reach = False
    self.deathtouch = False
    self.defender = False
    self.firststrike = False
    self.doublestrike = False
    self.menace = False
    self.trample = False
    self.haste = False
    self.power = -1
    self.toughness = -1
    self.cmc = -1
    self.colors = []
    self.types = []
    self.textLength = -1

def textLength_analysis(cards):
  #modulus text length by 5 to create buckets
  wTextLen = [0] * int(MAX_TEXT_LENGTH / TEXT_DIV); 
  bTextLen = [0] * int(MAX_TEXT_LENGTH / TEXT_DIV); 
  uTextLen = [0] * int(MAX_TEXT_LENGTH / TEXT_DIV); 
  rTextLen = [0] * int(MAX_TEXT_LENGTH / TEXT_DIV); 
  gTextLen = [0] * int(MAX_TEXT_LENGTH / TEXT_DIV); 
  cTextLen = [0] * int(MAX_TEXT_LENGTH / TEXT_DIV); 
  for card in cards:
    if len(card.colors) == 1:
      if card.colors[0] == "White":
        wTextLen[int(card.textLength / TEXT_DIV)] += 1 
      elif card.colors[0] == "Black":  
        bTextLen[int(card.textLength / TEXT_DIV)] += 1 
      elif card.colors[0] == "Blue":  
        uTextLen[int(card.textLength / TEXT_DIV)] += 1 
      elif card.colors[0] == "Red":  
        rTextLen[int(card.textLength / TEXT_DIV)] += 1 
      elif card.colors[0] == "Green":  
        gTextLen[int(card.textLength / TEXT_DIV)] += 1 
    else:
      #colorless or multicolored
      cTextLen[int(card.textLength / TEXT_DIV)] += 1 
  
  with open("textLengthAnalysis.dat", 'w') as outfile:
    for i in range(int(MAX_TEXT_LENGTH / TEXT_DIV)):
      outfile.write(str(i * TEXT_DIV))
      outfile.write("\t")
      outfile.write(str(wTextLen[i]))
      outfile.write("\t")
      outfile.write(str(uTextLen[i]))
      outfile.write("\t")
      outfile.write(str(bTextLen[i]))
      outfile.write("\t")
      outfile.write(str(rTextLen[i]))
      outfile.write("\t")
      outfile.write(str(gTextLen[i]))
      outfile.write("\t")
      outfile.write(str(cTextLen[i]))
      outfile.write("\n")

def color_analysis(cards):
  wManaCost = [0] * MAX_MANA_COST
  bManaCost = [0] * MAX_MANA_COST
  uManaCost = [0] * MAX_MANA_COST
  rManaCost = [0] * MAX_MANA_COST
  gManaCost = [0] * MAX_MANA_COST
  cManaCost = [0] * MAX_MANA_COST
  wCount = 0
  bCount = 0
  uCount = 0
  rCount = 0
  gCount = 0
  cCount = 0
  for card in cards:
    if len(card.colors) == 1:
      if card.colors[0] == "White":
        wManaCost[card.cmc] += 1 
        wCount += 1
      elif card.colors[0] == "Black":  
        bManaCost[card.cmc] += 1 
        bCount += 1
      elif card.colors[0] == "Blue":  
        uManaCost[card.cmc] += 1 
        uCount += 1
      elif card.colors[0] == "Red":  
        rManaCost[card.cmc] += 1 
        rCount += 1
      elif card.colors[0] == "Green":  
        gManaCost[card.cmc] += 1 
        gCount += 1
    else:
      #colorless or multicolored
      cManaCost[card.cmc] += 1 
      cCount += 1

  
  with open("colorAnalysis.dat", 'w') as outfile:
    for i in range(MAX_MANA_COST):
      outfile.write(str(wManaCost[i]))
      outfile.write("\t")
      outfile.write(str(uManaCost[i]))
      outfile.write("\t")
      outfile.write(str(bManaCost[i]))
      outfile.write("\t")
      outfile.write(str(rManaCost[i]))
      outfile.write("\t")
      outfile.write(str(gManaCost[i]))
      outfile.write("\t")
      outfile.write(str(cManaCost[i]))
      outfile.write("\n")
  

def instant_analysis(cards):
  wManaCost = [0] * MAX_MANA_COST
  bManaCost = [0] * MAX_MANA_COST
  uManaCost = [0] * MAX_MANA_COST
  rManaCost = [0] * MAX_MANA_COST
  gManaCost = [0] * MAX_MANA_COST
  cManaCost = [0] * MAX_MANA_COST
  wCount = 0
  bCount = 0
  uCount = 0
  rCount = 0
  gCount = 0
  cCount = 0
  for card in cards:
    if "Instant" in card.types:
      if len(card.colors) == 1:
        if card.colors[0] == "White":
          wManaCost[card.cmc] += 1 
          wCount += 1
        elif card.colors[0] == "Black":  
          bManaCost[card.cmc] += 1 
          bCount += 1
        elif card.colors[0] == "Blue":  
          uManaCost[card.cmc] += 1 
          uCount += 1
        elif card.colors[0] == "Red":  
          rManaCost[card.cmc] += 1 
          rCount += 1
        elif card.colors[0] == "Green":  
          gManaCost[card.cmc] += 1 
          gCount += 1
      else:
        #colorless or multicolored
        cManaCost[card.cmc] += 1 
        cCount += 1

  with open("instantAnalysis.dat", 'w') as outfile:
    for i in range(MAX_MANA_COST):
      outfile.write(str(wManaCost[i]))
      outfile.write("\t")
      outfile.write(str(uManaCost[i]))
      outfile.write("\t")
      outfile.write(str(bManaCost[i]))
      outfile.write("\t")
      outfile.write(str(rManaCost[i]))
      outfile.write("\t")
      outfile.write(str(gManaCost[i]))
      outfile.write("\t")
      outfile.write(str(cManaCost[i]))
      outfile.write("\n")

def sorcery_analysis(cards):
  wManaCost = [0] * MAX_MANA_COST
  bManaCost = [0] * MAX_MANA_COST
  uManaCost = [0] * MAX_MANA_COST
  rManaCost = [0] * MAX_MANA_COST
  gManaCost = [0] * MAX_MANA_COST
  cManaCost = [0] * MAX_MANA_COST
  wCount = 0
  bCount = 0
  uCount = 0
  rCount = 0
  gCount = 0
  cCount = 0
  for card in cards:
    if "Sorcery" in card.types:
      if len(card.colors) == 1:
        if card.colors[0] == "White":
          wManaCost[card.cmc] += 1 
          wCount += 1
        elif card.colors[0] == "Black":  
          bManaCost[card.cmc] += 1 
          bCount += 1
        elif card.colors[0] == "Blue":  
          uManaCost[card.cmc] += 1 
          uCount += 1
        elif card.colors[0] == "Red":  
          rManaCost[card.cmc] += 1 
          rCount += 1
        elif card.colors[0] == "Green":  
          gManaCost[card.cmc] += 1 
          gCount += 1
      else:
        #colorless or multicolor
        cManaCost[card.cmc] += 1 
        cCount += 1

  with open("sorceryAnalysis.dat", 'w') as outfile:
    for i in range(MAX_MANA_COST):
      outfile.write(str(wManaCost[i]))
      outfile.write("\t")
      outfile.write(str(uManaCost[i]))
      outfile.write("\t")
      outfile.write(str(bManaCost[i]))
      outfile.write("\t")
      outfile.write(str(rManaCost[i]))
      outfile.write("\t")
      outfile.write(str(gManaCost[i]))
      outfile.write("\t")
      outfile.write(str(cManaCost[i]))
      outfile.write("\n")

def creature_analysis(cards):
  wManaCost = [0] * MAX_MANA_COST
  bManaCost = [0] * MAX_MANA_COST
  uManaCost = [0] * MAX_MANA_COST
  rManaCost = [0] * MAX_MANA_COST
  gManaCost = [0] * MAX_MANA_COST
  cManaCost = [0] * MAX_MANA_COST
  wCount = 0
  bCount = 0
  uCount = 0
  rCount = 0
  gCount = 0
  cCount = 0
  for card in cards:
    if "Creature" in card.types: 
      if len(card.colors) == 1:
        if card.colors[0] == "White":
          wManaCost[card.cmc] += 1 
          wCount += 1
        elif card.colors[0] == "Black":  
          bManaCost[card.cmc] += 1 
          bCount += 1
        elif card.colors[0] == "Blue":  
          uManaCost[card.cmc] += 1 
          uCount += 1
        elif card.colors[0] == "Red":  
          rManaCost[card.cmc] += 1 
          rCount += 1
        elif card.colors[0] == "Green":  
          gManaCost[card.cmc] += 1 
          gCount += 1
      else:
        #colorless
        cManaCost[card.cmc] += 1 
        cCount += 1

  with open("creatureAnalysis.dat", 'w') as outfile:
    for i in range(MAX_MANA_COST):
      outfile.write(str(wManaCost[i]))
      outfile.write("\t")
      outfile.write(str(uManaCost[i]))
      outfile.write("\t")
      outfile.write(str(bManaCost[i]))
      outfile.write("\t")
      outfile.write(str(rManaCost[i]))
      outfile.write("\t")
      outfile.write(str(gManaCost[i]))
      outfile.write("\t")
      outfile.write(str(cManaCost[i]))
      outfile.write("\n")

def flying_analysis(cards):
  wManaCost = [0] * MAX_MANA_COST
  bManaCost = [0] * MAX_MANA_COST
  uManaCost = [0] * MAX_MANA_COST
  rManaCost = [0] * MAX_MANA_COST
  gManaCost = [0] * MAX_MANA_COST
  cManaCost = [0] * MAX_MANA_COST
  wSmallCount = 0
  wBigCount = 0
  bSmallCount = 0
  bBigCount = 0
  uSmallCount = 0
  uBigCount = 0
  rSmallCount = 0
  rBigCount = 0
  gSmallCount = 0
  gBigCount = 0
  cCount = 0
  for card in cards:
    if "Creature" in card.types:
      if card.flying:
        if len(card.colors) == 1:
          if card.colors[0] == "White":
            wManaCost[card.cmc] += 1 
            if card.power > 2:
              wBigCount += 1
            else:
              wSmallCount += 1
          elif card.colors[0] == "Black":  
            bManaCost[card.cmc] += 1 
            if card.power > 2:
              bBigCount += 1
            else:
              bSmallCount += 1
          elif card.colors[0] == "Blue":  
            uManaCost[card.cmc] += 1 
            if card.power > 2:
              uBigCount += 1
            else:
              uSmallCount += 1
          elif card.colors[0] == "Red":  
            rManaCost[card.cmc] += 1 
            if card.power > 2:
              rBigCount += 1
            else:
              rSmallCount += 1
          elif card.colors[0] == "Green":  
            gManaCost[card.cmc] += 1 
            if card.power > 2:
              gBigCount += 1
            else:
              gSmallCount += 1
        else:
          #colorless
          cManaCost[card.cmc] += 1 
          cCount += 1

  with open("flyingAnalysis.dat", 'w') as outfile:
    for i in range(MAX_MANA_COST):
      outfile.write(str(wManaCost[i]))
      outfile.write("\t")
      outfile.write(str(uManaCost[i]))
      outfile.write("\t")
      outfile.write(str(bManaCost[i]))
      outfile.write("\t")
      outfile.write(str(rManaCost[i]))
      outfile.write("\t")
      outfile.write(str(gManaCost[i]))
      outfile.write("\t")
      outfile.write(str(cManaCost[i]))
      outfile.write("\n")


def read_in_cards(fpath,cards):
  with open(fpath) as infile:
    for line in infile:
      cards.append(Card(line.strip()))


def card_lookup(card):
  url = "https://api.magicthegathering.io/v1/cards?name=\"" + card.name + "\""
  response = requests.get(url).text
  output = json.loads(response)
  #pprint(output)
  if len(output['cards']) == 0:
    print("Card: \"" + card.name + "\" is invalid")
  else:
    parse_json(card,output)

def parse_json(card,output):
  cardText = output['cards'][0]
  card.types = cardText['types']
  card.cmc = int(cardText['cmc'])
  card.textLength = len(cardText['text'].split())
  try:
    card.colors = cardText['colors']
  except KeyError:
    print("Card \"", card.name, "\" has empty colors")

  if "Creature" in card.types:
    
    #catch variable power or toughness
    try:
      card.toughness = int(cardText['toughness'])
    except:
      pass
    try:  
      card.power = int(cardText['power'])
    except:
      pass
    
    if re.match('.*[Ff]lying',cardText['text']):
      card.flying = True
    if re.match('.*[Rr]each',cardText['text']):
      card.reach = True
    if re.match('.*[Dd]efender',cardText['text']):
      card.defender = True
    if re.match('.*[Ff]irst [Ss]trike',cardText['text']):
      card.firststrike = True
    if re.match('.*[Dd]ouble [Ss]trike',cardText['text']):
      card.doublestrike = True
    if re.match('.*[Mm]enace',cardText['text']):
      card.menace = True
    if re.match('.*[Tt]rample',cardText['text']):
      card.trample = True
    if re.match('.*[Hh]aste',cardText['text']):
      card.haste = True

cards = []
read_in_cards("../Cards/White",cards)
read_in_cards("../Cards/Black",cards)
read_in_cards("../Cards/Red",cards)
read_in_cards("../Cards/Blue",cards)
read_in_cards("../Cards/Green",cards)
read_in_cards("../Cards/Artifact",cards)
read_in_cards("../Cards/Land",cards)
read_in_cards("../Cards/Multicolor",cards)

counter = 0
start = time.time()
for card in cards:
  card_lookup(card)
  counter += 1
end = time.time()

print("Searched for all ", counter, " cards in ", (end-start), " seconds.") 

color_analysis(cards)
creature_analysis(cards)
instant_analysis(cards)
sorcery_analysis(cards)
flying_analysis(cards)
textLength_analysis(cards)
