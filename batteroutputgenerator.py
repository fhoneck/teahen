import pandas as pd
import numpy as np
import os

#LEAGUE MODIFIERS
la_bb = .09
la_k = .22
la_avg = .25
la_obp = .325
la_iso = .170
la_babip = .295
thisyear = 2022

#IMPORT STEAMER
steamer = pd.read_csv("steamerbat.csv")
steamer["bb"] = (steamer["BB"] / steamer ["PA"] / 0.09)*100
steamer["k"] = (steamer["SO"] / steamer ["PA"] / 0.22)*100
steamer["iso"] = ((steamer["SLG"] - steamer["AVG"]) / 0.17)*100
steamer["babip"] = ((steamer["H"] - steamer["HR"]) / (steamer["AB"] - steamer["HR"] - steamer["SO"]) / 0.295)*100
steamer["def"] = steamer["Def"]

#ATTACH AGES
agesheet = pd.read_csv("hitagedict.csv")
steamer = steamer.merge(agesheet, on = "playerid")

#OVERRULE HITTERS
overruled = pd.read_csv("overruledbat.csv")
overruledlist = list(overruled["playerid"].astype(str))
steamerlist = list(steamer["playerid"].astype(str))
for index, row in steamer.iterrows():
    if str(row["playerid"]) in overruledlist:
        steamer.loc[index, "bb"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["bb"]
        steamer.loc[index, "k"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["k"]
        steamer.loc[index, "iso"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["iso"]
        steamer.loc[index, "babip"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["babip"]
        steamer.loc[index, "def"] = overruled[overruled["playerid"].astype(str) == str(row["playerid"])].iloc[0]["def"]
steamer["playerid"] = steamer["playerid"].astype(str)

#ADD OVERRULED GUYS
for index, row in overruled.iterrows():
    if str(row["playerid"]) not in steamerlist:
        steamer.loc[len(steamer), "bb"] = row["bb"]
        steamer.loc[len(steamer)-1, "k"] = row["k"]
        steamer.loc[len(steamer)-1, "playerid"] = row["playerid"]
        steamer.loc[len(steamer)-1, "Age"] = row["Age"]
        steamer.loc[len(steamer)-1, "iso"] = row["iso"]
        steamer.loc[len(steamer)-1, "Name_x"] = row["Name"]
        steamer.loc[len(steamer)-1, "babip"] = row["babip"]
        steamer.loc[len(steamer)-1, "def"] = row["def"]
steamer["playerid"] = steamer["playerid"].astype(str)

#TALENT CHANGE AVERAGE MODIFIERS
bb_dic = {17:12, 18: 12,
		19: 10,
		20: 8,
		21: 6,
		22: 4,
		23: 3,
		24: 2,
		25: 1,
		26: 1,
		27: 1,
		28: 1,
		29: 0,
		30: -1,
		31: -1,
		32: -1,
		33: -1,
		34: -2,
		35: -2,
		36: -2,
		37: -2,
		38: -3,
		39: -3,
		40: -3
		}

k_dic = {17:-14,18: -14,
		19: -12,
		20: -10,
		21: -8,
		22: -7,
		23: -6,
		24: -5,
		25: -4,
		26: -3,
		27: -2,
		28: -1,
		29: -1,
		30: 0,
		31: 0,
		32: 1,
		33: 1,
		34: 2,
		35: 2,
		36: 2,
		37: 3,
		38: 3,
		39: 3,
		40: 3
		}

iso_dic = {17:10,18: 10,
		19: 8,
		20: 6,
		21: 3,
		22: 2,
		23: 1,
		24: 1,
		25: 1,
		26: 1,
		27: -1,
		28: -2,
		29: -2,
		30: -2,
		31: -3,
		32: -4,
		33: -5,
		34: -6,
		35: -7,
		36: -8,
		37: -9,
		38: -10,
		39: -11,
		40: -12
		}

babip_dic = {17:0,18: 0,
		19: 0,
		20: 0,
		21: 0,
		22: 0,
		23: 0,
		24: 0,
		25: 0,
		26: -1,
		27: -1,
		28: -1,
		29: -1,
		30: -1,
		31: -2,
		32: -2,
		33: -2,
		34: -2,
		35: -3,
		36: -3,
		37: -3,
		38: -4,
		39: -4,
		40: -4
		}

def_dic = {17:0,18: 0,
		19: 1,
		20: 1,
		21: 1,
		22: 1,
		23: 0,
		24: 0,
		25: 0,
		26: 0,
		27: 0,
		28: -1,
		29: -1,
		30: -1,
		31: -2,
		32: -2,
		33: -2,
		34: -2,
		35: -2,
		36: -2,
		37: -2,
		38: -2,
		39: -2,
		40: -2
		}

#RUN SIMS
output = []
talent = []
tableau = []

for index, row in steamer.iterrows():
    #os.system("cls")
    print("Running career for player #" + str(index) + " / " + str(steamer.shape[0]))
    try:
        p_name = row["Name_x"]
        p_age = int(row["Age"])
        p_bb = row["bb"]
        p_k = row["k"]
        p_iso = row["iso"]
        p_babip = row["babip"]
        p_def = row["def"]
        p_id = row["playerid"]
        year = thisyear
        output = []
        talent = []
        for i in range(p_age,60):
            #AGE UP
            try:
                bb = p_bb
                k = p_k
                iso = p_iso
                babip = p_babip
                defe = p_def
                #CONVERSION WITH LEAGUE MODIFIERS
                bb_real = bb*la_bb/100
                k_real = k*la_k/100
                iso_real = iso*la_iso/100
                babip_real = babip*la_babip/100
                avg_real = la_avg * (23.94 -0.176*k + .824*babip + .114*iso)/100
                obp_real = la_obp * (27.28 + .183*bb -.119*k + .581*babip +.082*iso)/100
                slg_real = avg_real + iso_real
                ops_real = obp_real + slg_real
                war = -12.26 + 19.317*ops_real + .112*defe
                if row["Team"] == "Rockies":
                    war -= 1
                #if war > -0.5:
                tableau.append([year, p_name, p_id, p_age, bb_real, k_real, iso_real, babip_real, avg_real, obp_real, slg_real, ops_real, defe, war])
                talent.append([p_age,p_bb,p_k,p_iso,p_babip,p_def])
                year += 1
                p_age += 1
                #TALENT DEVELOPMENT
                p_bb = (p_bb) * (100 + bb_dic[i])/100
                p_k = (p_k) * (100 + k_dic[i])/100
                p_iso = (p_iso) * (100 + iso_dic[i])/100
                p_babip = (p_babip) * (100 + babip_dic[i])/100
                p_def = (p_def + def_dic[i])
            except:
                pass
                #tableau.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                #talent.append([0,0,0,0,0,0])
    except:
        pass

o = pd.DataFrame(tableau)
o.columns = ["Year","Name","PlayerID","Age", "BB%","K%","ISO","BABIP", "AVG", "OBP", "SLG", "OPS", "DEF", "WAR"]
o["BB%"] = round(o["BB%"]*100,1)
o["K%"] = round(o["K%"]*100,1)
o["ISO"] = round(o["ISO"],3)
o["BABIP"] = round(o["BABIP"],3)
o["AVG"] = round(o["AVG"],3)
o["OBP"] = round(o["OBP"],3)
o["SLG"] = round(o["SLG"],3)
o["OPS"] = round(o["OPS"],3)
o["DEF"] = round(o["DEF"],1)
o["WAR"] = round(o["WAR"],1)
t = pd.DataFrame(talent)
t.columns = ["Age", "bb","k","iso","babip", "def"]

uniqueplayers = o["PlayerID"].unique()

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
	bb = o[o["PlayerID"] == i]["BB%"].tolist()
	k = o[o["PlayerID"] == i]["K%"].tolist()
	iso = o[o["PlayerID"] == i]["ISO"].tolist()
	babip = o[o["PlayerID"] == i]["BABIP"].tolist()
	avg = o[o["PlayerID"] == i]["AVG"].tolist()
	obp = o[o["PlayerID"] == i]["OBP"].tolist()
	slg = o[o["PlayerID"] == i]["SLG"].tolist()
	ops = o[o["PlayerID"] == i]["OPS"].tolist()
	defe = o[o["PlayerID"] == i]["DEF"].tolist()
	war = o[o["PlayerID"] == i]["WAR"].tolist()
	for x in range(0,l):
		line.append(bb[x])
		line.append(k[x])
		line.append(iso[x])
		line.append(babip[x])
		line.append(avg[x])
		line.append(obp[x])
		line.append(slg[x])
		line.append(ops[x])
		line.append(defe[x])
		line.append(war[x])
	realoutput.append(line)

real = pd.DataFrame(realoutput)
colnames = ["Name","PlayerID",str(thisyear) + " Age"]
for i in range(0,10):
	colnames.append(str(thisyear + i) + " BB%")
	colnames.append(str(thisyear + i) + " K%")
	colnames.append(str(thisyear + i) + " ISO")
	colnames.append(str(thisyear + i) + " BABIP")
	colnames.append(str(thisyear + i) + " AVG")
	colnames.append(str(thisyear + i) + " OBP")
	colnames.append(str(thisyear + i) + " SLG")
	colnames.append(str(thisyear + i) + " OPS")
	colnames.append(str(thisyear + i) + " DEF")
	colnames.append(str(thisyear + i) + " WAR")
real.columns = colnames
real.to_csv("Teahen Batters " + str(pd.datetime.now().date()) + ".csv")