import pandas as pd

#LEAGUE MODIFIERS
la_bb = 3.25
la_k = 8.75
la_hr = 1.35
la_era = 4.45
thisyear = 2022

#IMPORT STEAMER
steamer = pd.read_csv("steamerpitch.csv")
steamer["bb"] = (steamer["BB/9"] / la_bb)*100
steamer["k"] = (steamer["K/9"] / la_k)*100
steamer["hr"] = ((steamer["HR"] / steamer["IP"]) * 9 / 1.25)*100

#ATTACH AGES
agesheet = pd.read_csv("pitchagedict.csv")
steamer = steamer.merge(agesheet, on = "playerid")

#REPLACE OVERRULED GUYS
#overruled = pd.read_csv("overruledpitch.csv")
#overruledlist = list(overruled["playerid"].astype(str))
#steamerlist = list(steamer["playerid"].astype(str))
#for index, row in steamer.iterrows():
#    if str(row["playerid"]) in overruledlist:
#        steamer.loc[index, "bb"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["bb"]
#        steamer.loc[index, "k"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["k"]
#        steamer.loc[index, "hr"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["hr"]

#ADD OVERRULED GUYS
#for index, row in overruled.iterrows():
#    if str(row["playerid"]) not in steamerlist:
#        steamer.loc[len(steamer), "bb"] = row["bb"]
#        steamer.loc[len(steamer)-1, "k"] = row["k"]
#        steamer.loc[len(steamer)-1, "playerid"] = row["playerid"]
#        steamer.loc[len(steamer)-1, "Age"] = row["Age"]
#        steamer.loc[len(steamer)-1, "hr"] = row["hr"]
#        steamer.loc[len(steamer)-1, "Name_x"] = row["Name"]
#        steamer.loc[len(steamer)-1, "IP"] = row["IP"]
#steamer["playerid"] = steamer["playerid"].astype(str)
#steamer.to_csv("steamerpitchout.csv")

#TALENT CHANGE AVERAGE MODIFIERS
bb_dic = {17: -12, 18: -12,
		19: -10,
		20: -10,
		21: -10,
		22: -10,
		23: -6,
		24: -4,
		25: -2,
		26: 0,
		27: 0,
		28: 1,
		29: 2,
		30: 2,
		31: 2,
		32: 2,
		33: 2,
		34: 2,
		35: 2,
		36: 3,
		37: 3,
		38: 3,
		39: 3,
		40: 4
		}

k_dic = {17: 4,18: 4,
		19: 4,
		20: 2,
		21: 1,
		22: 0,
		23: 0,
		24: -1,
		25: -1,
		26: -1,
		27: -1,
		28: -2,
		29: -2,
		30: -2,
		31: -3,
		32: -3,
		33: -3,
		34: -3,
		35: -3,
		36: -4,
		37: -5,
		38: -6,
		39: -7,
		40: -8
		}

hr_dic = {17:-6,18: -6,
		19: -6,
		20: -6,
		21: -6,
		22: -5,
		23: -3,
		24: -1,
		25: 0,
		26: 1,
		27: 2,
		28: 3,
		29: 4,
		30: 4,
		31: 4,
		32: 4,
		33: 4,
		34: 5,
		35: 6,
		36: 7,
		37: 8,
		38: 8,
		39: 8,
		40: 8
		}

#MAKE OUTPUT
output = []
talent = []
#complete = []
tableau = []

for index, row in steamer.iterrows():
    print("Running career for player #" + str(index) + " / " + str(steamer.shape[0]))
    try:
        p_name = row["Name_x"]
        p_age = int(row["Age"])
        p_bb = row["bb"]
        p_k = row["k"]
        p_hr = row["hr"]
        ip = row["IP"]
        p_id = row["playerid"]
        year = thisyear
        output = []
        talent = []
        for i in range(p_age,60):
            
            try:
                #PRODUCTION RANDOMNESS
                bb = p_bb
                k = p_k
                hr = p_hr
                #CONVERSION WITH LEAGUE MODIFIERS
                bb_real = bb*la_bb/100
                k_real = k*la_k/100
                hr_real = hr*la_hr/100
                ktotal_real = round(k_real*ip/9,0)
                bbtotal_real = round(bb_real*ip/9,0)
                hrtotal_real = round(hr_real*ip/9,0)
                fip_real = 3.24 + (13*hr_real + 3*bb_real - 2*k_real)/9
                era_real = fip_real - .45 + .06*k_real - .016*bb_real - .105*hr_real
                warip = .053832 - .01*fip_real
                war = warip*ip
                if row["Team"] == "Rockies":
                    war += ip / 200
                #if war > -0.2:
                tableau.append([year, p_name,row["Team"], p_id, p_age, ip, k_real, bb_real, hr_real, ktotal_real, bbtotal_real, hrtotal_real, fip_real, era_real, war])
                talent.append([p_age,p_bb,p_k,p_hr])
                #AGE UP
                year += 1
                p_age += 1
                #TALENT DEVELOPMENT
                p_bb = (p_bb) * (100 + bb_dic[i])/100
                p_k = (p_k) * (100 + k_dic[i])/100
                p_hr = (p_hr) * (100 + hr_dic[i])/100
            except:
                pass
        o = pd.DataFrame(tableau)
        o.columns = ["Year", "Name","Team","PlayerID", "Age", "IP", "K/9","BB/9","HR/9","SO", "BB", "HR", "FIP", "ERA", "WAR"]
        o["BB/9"] = round(o["BB/9"],2)
        o["K/9"] = round(o["K/9"],2)
        o["HR/9"] = round(o["HR/9"],2)
        o["SO"] = round(o["SO"],0)
        o["BB"] = round(o["BB"],0)
        o["HR"] = round(o["HR"],0)
        o["FIP"] = round(o["FIP"],2)
        o["ERA"] = round(o["ERA"],2)
        o["WAR"] = round(o["WAR"],1)
        t = pd.DataFrame(talent)
        t.columns = ["Age", "bb","k","iso","babip", "def"]
        #complete.append([row["Name_x"],row["Team"], row["Age"],o["WAR"][0],o["WAR"][1],o["WAR"][2],o["WAR"][3],o["WAR"][4],o["WAR"][5],o["WAR"][6],o["WAR"][7],o["WAR"][8],o["WAR"][9],o["WAR"][10],o["WAR"][11]])
    except:
        pass
    
uniqueplayers = o["PlayerID"].unique()

o.to_csv("TRY THIS.csv")

realoutput = []
printcount = 0
for i in uniqueplayers:
	printcount += 1
	print("Formatting output for player #" + str(printcount) + " / " + str(len(uniqueplayers)))
	line = []
	l = len(o[o["PlayerID"] == i]["WAR"].tolist())
	if l > 10:
		l = 10
	line.insert(0,o[o["PlayerID"] == i]["Name"].tolist()[0])
	line.insert(1,o[o["PlayerID"] == i]["PlayerID"].tolist()[0])
	line.insert(2,o[o["PlayerID"] == i]["Age"].tolist()[0])
	line.insert(3,o[o["PlayerID"] == i]["IP"].tolist()[0])
	bb9 = o[o["PlayerID"] == i]["BB/9"].tolist()
	k9 = o[o["PlayerID"] == i]["K/9"].tolist()
	hr9 = o[o["PlayerID"] == i]["HR/9"].tolist()
	so = o[o["PlayerID"] == i]["SO"].tolist()
	bb = o[o["PlayerID"] == i]["BB"].tolist()
	hr = o[o["PlayerID"] == i]["HR"].tolist()
	fip = o[o["PlayerID"] == i]["FIP"].tolist()
	era = o[o["PlayerID"] == i]["ERA"].tolist()
	war = o[o["PlayerID"] == i]["WAR"].tolist()
	for x in range(0,l):
		line.append(bb9[x])
		line.append(k9[x])
		line.append(hr9[x])
		line.append(so[x])
		line.append(bb[x])
		line.append(hr[x])
		line.append(fip[x])
		line.append(era[x])
		line.append(war[x])
	realoutput.append(line)

real = pd.DataFrame(realoutput)
colnames = ["Name","PlayerID", str(thisyear) + " Age", "IP"]
for i in range(0,10):
	colnames.append(str(thisyear + i) + " BB/9")
	colnames.append(str(thisyear + i) + " K/9")
	colnames.append(str(thisyear + i) + " HR/9")
	colnames.append(str(thisyear + i) + " SO")
	colnames.append(str(thisyear + i) + " BB")
	colnames.append(str(thisyear + i) + " HR")
	colnames.append(str(thisyear + i) + " FIP")
	colnames.append(str(thisyear + i) + " ERA")
	colnames.append(str(thisyear + i) + " WAR")
real.columns = colnames
real.to_csv("Teahen Pitchers " + str(pd.datetime.now().date()) + ".csv")