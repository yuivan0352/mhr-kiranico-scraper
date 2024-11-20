import requests
import json
import sys
from bs4 import BeautifulSoup

def scrapePage(url):
    URL = url
    page = requests.get(URL)
    page = page.text.encode('ascii', 'ignore').decode('ascii')

    soup = BeautifulSoup(page, "html.parser")
    return soup

currentPage = scrapePage("https://mhrise.kiranico.com/")

#Scraping Home Page
links = {}
linkKeywords = {"armors?", "weapons?", "material", "view=lg", "view=event", "view=hub_high", "view=hub_low", "view=hub_master", "view=mystery"}

for link in currentPage.find_all('a'):
    linkString = str(link.get('href'))
    if (linkString.find("data") != -1):
        for word in linkKeywords:
            if (linkString.find(word) != -1):
                links.setdefault(link.get_text(), link.get('href'))

links = dict(sorted(links.items(), key=lambda item: item[1]))

#Scraping Armor Pages
armorLinks = []
armors = []
armorIds = {}

for link in links.values():
    if (link.find("armor") != -1):
        armorLinks.append(link)

i = 0
for link in armorLinks:
    currentPage = scrapePage(link)
    armorType = 0
    armorSet = ""

    for armor in currentPage.table.find_all('a'):
        currentArmor = {}
        currentArmor.update({"id": i})
        if (armor.get('href').find("skills") == -1):
            currentArmorSet = ""
            currentPage = scrapePage(armor.get('href'))
            if armorIds.get(currentPage.h1.get_text("", True)) != None:
                continue
            else:
                armorIds.update({currentPage.h1.get_text("", True): i})
            currentArmor.update({"name": currentPage.h1.get_text("", True)})
            for j in range(len(currentArmor.get("name"))):
                if (currentArmor.get("name")[j] != " "):
                    currentArmorSet += currentArmor.get("name")[j]
                else: break
            if (currentArmorSet != armorSet or not armorSet): 
                armorType = 0
                armorSet = currentArmorSet
            match armorType:
                case 0:
                    currentArmor.update({"type": "head"})
                case 1:
                    currentArmor.update({"type": "chest"})
                case 2:
                    currentArmor.update({"type": "arms"})
                case 3:
                    currentArmor.update({"type": "waist"})
                case 4:
                    currentArmor.update({"type": "legs"})
            armorType += 1
            materials = {}
            for mats in currentPage.find_all('table')[1].find_all('a'):
                materials.update({mats.get_text(): mats.parent.next_sibling.next_sibling.text})
            currentArmor.update({"materials": materials})
            armors.append(currentArmor)
            print(currentArmor)
            i += 1

with open("armors.json", "w") as writeFile:
    json.dump(armors, writeFile)

#Scraping Weapon Pages
weaponLinks = []
weaponDict = {}
weapons = []
weaponIds = {}

for link in links.values():
    if (link.find("weapons") != -1):
        weaponLinks.append(link)

for link in weaponLinks:
    weaponNum = ""
    for i in reversed(range(len(link))):
        if (link[i].isdigit()):
            weaponNum = link[i] + weaponNum
        else:
            break    
    weaponNum = int(weaponNum)
    weaponDict.setdefault(weaponNum, link)

weaponDict = dict(sorted(weaponDict.items()))

i = 0
for weaponNum in weaponDict:
    currentPage = scrapePage(weaponDict.get(weaponNum))
    for weapon in currentPage.table.find_all('a'):
        currentWeapon = {}
        currentWeapon.update({"id": i})
        currentPage = scrapePage(weapon.get('href'))
        currentWeapon.update({"name": currentPage.h1.get_text("", True)})
        weaponIds.update({currentWeapon.get("name"): i})
        match weaponNum:
            case 0:
                currentWeapon.update({"type": "Great Sword"})
            case 1:
                currentWeapon.update({"type": "Sword & Shield"})
            case 2:
                currentWeapon.update({"type": "Dual Blades"})
            case 3:
                currentWeapon.update({"type": "Long Sword"})
            case 4:
                currentWeapon.update({"type": "Hammer"})
            case 5:
                currentWeapon.update({"type": "Hunting Horn"})
            case 6:
                currentWeapon.update({"type": "Lance"})
            case 7:
                currentWeapon.update({"type": "Gunlance"})
            case 8:
                currentWeapon.update({"type": "Switch Axe"})
            case 9:
                currentWeapon.update({"type": "Charge Blade"})
            case 10:
                currentWeapon.update({"type": "Insect Glaive"})
            case 11:
                currentWeapon.update({"type": "Bow"})
            case 12:
                currentWeapon.update({"type": "Heavy Bowgun"})
            case 13:
                currentWeapon.update({"type": "Light Bowgun"})
        forgingMats = {}
        upgradeMats = {}
        if (weaponNum != 12 and weaponNum != 13):
            for mats in currentPage.find_all('table')[1].find_all('a'):
                forgingMats.update({mats.get_text(): mats.parent.next_sibling.next_sibling.text})
            for mats in currentPage.find_all('table')[2].find_all('a'):
                upgradeMats.update({mats.get_text(): mats.parent.next_sibling.next_sibling.text})
        else:
            for mats in currentPage.find_all('table')[6].find_all('a'):
                forgingMats.update({mats.get_text(): mats.parent.next_sibling.next_sibling.text})
            for mats in currentPage.find_all('table')[7].find_all('a'):
                upgradeMats.update({mats.get_text(): mats.parent.next_sibling.next_sibling.text})
        currentWeapon.update({"forgingMats": forgingMats})
        currentWeapon.update({"upgradeMats": upgradeMats})
        weapons.append(currentWeapon)
        print(currentWeapon)
        i += 1

with open("weapons.json", "w") as writeFile:
    json.dump(weapons, writeFile)

#Scraping Material Pages
materialLinks = []
materials = []
materialIds = {}

currentPage = scrapePage(links.get("Materials"))
i = 0
for mat in currentPage.article.find_all('a'):
    currentPage = scrapePage(mat.get('href'))
    tables = currentPage.find_all("table")
    currentMat = {}
    matWeapons = []
    matArmors = []
    currentMat.update({"id": i})
    currentMat.update({"name": currentPage.h1.get_text("", True)})
    materialIds.update({currentMat.get("name"): i})

    if (len(tables) == 3 and currentPage.find("tr") != None):
        for weapon in tables[0].find_all('a'):
            matWeapons.append(weaponIds.get(weapon.get_text()))
        for armor in tables[1].find_all('a'):
            matArmors.append(armorIds.get(armor.get_text()))
    elif (len(tables) == 4 and (tables[1].find("tr") != None or tables[2].find("tr") != None)):
        for weapon in tables[1].find_all('a'):
            matWeapons.append(weaponIds.get(weapon.get_text()))
        for armor in tables[2].find_all('a'):
            matArmors.append(armorIds.get(armor.get_text()))
    elif (len(tables) == 5 and (tables[2].find("tr") != None or tables[3].find("tr") != None)):
        for weapon in tables[2].find_all('a'):
            matWeapons.append(weaponIds.get(weapon.get_text()))
        for armor in tables[3].find_all('a'):
            matArmors.append(armorIds.get(armor.get_text()))
    else:
        continue
    currentMat.update({"Weapons": matWeapons})
    currentMat.update({"Armors": matArmors})
    i += 1
    print(currentMat)

with open("materials.json", "w") as writeFile:
    json.dump(materials, writeFile)