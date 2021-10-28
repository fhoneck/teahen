import streamlit as st
import pandas as pd

st.set_page_config(layout = "wide")

st.title("PROJECTIONS v2")
topcol1, topcol2 = st.columns([1,3])
page = topcol1.selectbox("Page",("All Players","Player Profile","Create Career"))
agelimit = 40
if page == "All Players":

    pitchers = pd.read_csv("TRY THIS.csv")
    with st.form(key="columns_in_form"):
        col1, col2, col3, col4 = st.columns([2,1,1,1])
        years = col1.slider("Seasons",2022,2035,(2022,2023))
        warlimit = col2.number_input("WAR Minimum",-1.0,0.0,0.0,0.1)
        teams = list(set(list(pitchers["Team"].astype(str))))
        teams.append(" Any")
        teams = sorted(teams)
        team = col3.selectbox("Team",teams)
        totalstats = col4.radio("Leaderboard",("Season","Total"))
        st.form_submit_button("Submit")
    


    pitchers = pitchers[["Year","Name","Team","Age","WAR","FIP","ERA","IP","K/9","BB/9","HR/9","SO","BB","HR","PlayerID"]]

    pitchers = pitchers[pitchers["Age"]<= agelimit]
    pitchers = pitchers[pitchers["WAR"]>= warlimit]
    pitchers = pitchers[pitchers["Year"]>=years[0]]
    pitchers = pitchers[pitchers["Year"]<=years[1]]
    if team != " Any":
        pitchers = pitchers[pitchers["Team"]==team]

    if totalstats == "Total":
        pitchers["temp"] = pitchers["Age"]
        pitchers = pitchers.groupby(by=["Name","Team", "PlayerID"],as_index=False).agg({"WAR":"sum","FIP":"mean","ERA":"mean","IP":"sum","K/9":"mean","BB/9":"mean","HR/9":"mean","SO":"sum","BB":"sum","HR":"sum","Age": "min","temp":"max"})
        pitchers["Age"] = pitchers["Age"].astype(str) + "-" + pitchers["temp"].astype(str)
        pitchers = pitchers[["Name","Team","Age","WAR","FIP","ERA","IP","K/9","BB/9","HR/9","SO","BB","HR","PlayerID"]]
    with st.spinner("Loading sheet... may be slow when loading many rows"):
        st.dataframe(pitchers.sort_values(by = "WAR",ascending = False).style.format({"FIP":"{:.2f}","ERA":"{:.2f}","K/9":"{:.2f}","BB/9":"{:.2f}","HR/9":"{:.2f}","WAR":"{:.1f}","IP":"{:.0f}","SO":"{:.0f}","HR":"{:.0f}","BB":"{:.0f}"}),height = 800)

    st.download_button("Download as CSV",data = pitchers.to_csv(),file_name="Summary Sheet.csv")

if page == "Player Profile":
    pitchers = pd.read_csv("TRY THIS.csv")
    pitchers = pitchers[pitchers["Age"]<= agelimit]
    pitchers["Combo"] = pitchers["Name"] + " (" + pitchers["PlayerID"].astype(str) + ")"
    pitcherlist = sorted(list(set(list(pitchers["Combo"]))))
    player = topcol2.selectbox("Select Player",pitcherlist)
    pitchers = pitchers[pitchers["Combo"]== player]
    name = pitchers["Name"].iloc[0]
    st.header(name)
    #CAREER TOTALS
    st.caption("Career Totals")
    career = pitchers
    career["temp"] = career["Age"]
    career = career[career["WAR"]>= 0]
    career = career.groupby(by=["Name", "PlayerID"],as_index=False).agg({"WAR":"sum","FIP":"mean","ERA":"mean","IP":"sum","K/9":"mean","BB/9":"mean","HR/9":"mean","SO":"sum","BB":"sum","HR":"sum","Age": "min","temp":"max"})
    career["Age"] = career["Age"].astype(str) + "-" + career["temp"].astype(str)
    career = career[["Name","Age","WAR","FIP","ERA","IP","K/9","BB/9","HR/9","SO","BB","HR","PlayerID"]]
    career.set_index("Name",inplace = True)
    st.dataframe(career.sort_values(by = "Age").style.format({"FIP":"{:.2f}","ERA":"{:.2f}","K/9":"{:.2f}","BB/9":"{:.2f}","HR/9":"{:.2f}","WAR":"{:.1f}","IP":"{:.0f}","SO":"{:.0f}","HR":"{:.0f}","BB":"{:.0f}"}),height = 800)
    #SEASONS
    st.caption("Seasons")
    pitchers = pitchers[["Year","Age","WAR","FIP","ERA","IP","K/9","BB/9","HR/9","SO","BB","HR"]]
    pitchers.set_index("Year", inplace = True)
    st.dataframe(pitchers.sort_values(by = "Age").style.format({"FIP":"{:.2f}","ERA":"{:.2f}","K/9":"{:.2f}","BB/9":"{:.2f}","HR/9":"{:.2f}","WAR":"{:.1f}","IP":"{:.0f}","SO":"{:.0f}","HR":"{:.0f}","BB":"{:.0f}"}),height = 800)
    st.download_button("Download as CSV",data = pitchers.to_csv(),file_name=name + ".csv")

if page == "Create Career":
    la_bb = 3.25
    la_k = 8.75
    la_hr = 1.35
    la_era = 4.45
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
    thisyear = 2022
    st.subheader("Bio")
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("Name")
    age = col2.number_input("Age",18,40,18,1)
    pos = col3.radio("Position",("Starter","Reliever"))
    st.subheader("Skills")
    st.write("Instructions: Skills are relative to league averages, where 100 is average. A higher number indicates more frequency, which is good or bad, depending on the statistic.")
    col1, col2, col3 = st.columns(3)
    k = col1.slider("Strikeouts",0,200,80)
    bb = col2.slider("Walks",0,200,120)
    hr = col3.slider("Home Runs",0,200,120)
    st.subheader("Projections")
    p_name = name
    p_age = age
    p_bb = bb
    p_k = k
    p_hr = hr
    if pos == "Starter":
        ip = 200
    elif pos == "Reliever":
        ip = 65
    year = thisyear
    output = []
    talent = []
    tableau = []
    for i in range(p_age,41):
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
            #if war > -0.2:
            tableau.append([year, p_name, p_age, ip, k_real, bb_real, hr_real, ktotal_real, bbtotal_real, hrtotal_real, fip_real, era_real, war])
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
    o.columns = ["Year", "Name", "Age", "IP", "K/9","BB/9","HR/9","SO", "BB", "HR", "FIP", "ERA", "WAR"]
    o["BB/9"] = round(o["BB/9"],2)
    o["K/9"] = round(o["K/9"],2)
    o["HR/9"] = round(o["HR/9"],2)
    o["SO"] = round(o["SO"],0)
    o["BB"] = round(o["BB"],0)
    o["HR"] = round(o["HR"],0)
    o["FIP"] = round(o["FIP"],2)
    o["ERA"] = round(o["ERA"],2)
    o["WAR"] = round(o["WAR"],1)
    st.caption("Career Totals")
    career = o
    pitchers = o
    career["temp"] = career["Age"]
    career = career[career["WAR"]>= 0]
    career = career.groupby(by=["Name"],as_index=False).agg({"WAR":"sum","FIP":"mean","ERA":"mean","IP":"sum","K/9":"mean","BB/9":"mean","HR/9":"mean","SO":"sum","BB":"sum","HR":"sum","Age": "min","temp":"max"})
    career["Age"] = career["Age"].astype(str) + "-" + career["temp"].astype(str)
    career = career[["Name","Age","WAR","FIP","ERA","IP","K/9","BB/9","HR/9","SO","BB","HR"]]
    career.set_index("Name",inplace = True)
    st.dataframe(career.sort_values(by = "Age").style.format({"FIP":"{:.2f}","ERA":"{:.2f}","K/9":"{:.2f}","BB/9":"{:.2f}","HR/9":"{:.2f}","WAR":"{:.1f}","IP":"{:.0f}","SO":"{:.0f}","HR":"{:.0f}","BB":"{:.0f}"}),height = 800)
    #SEASONS
    st.caption("Seasons")
    pitchers = pitchers[["Year","Age","WAR","FIP","ERA","IP","K/9","BB/9","HR/9","SO","BB","HR"]]
    pitchers.set_index("Year", inplace = True)
    st.dataframe(pitchers.sort_values(by = "Age").style.format({"FIP":"{:.2f}","ERA":"{:.2f}","K/9":"{:.2f}","BB/9":"{:.2f}","HR/9":"{:.2f}","WAR":"{:.1f}","IP":"{:.0f}","SO":"{:.0f}","HR":"{:.0f}","BB":"{:.0f}"}),height = 800)
    st.download_button("Download as CSV",data = pitchers.to_csv(),file_name=name + ".csv")