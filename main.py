from lxml import html
import requests

#Parses input for Team School and Code
sinput = input().rstrip()
targetschool = sinput[:-3]
targetteam = sinput[-2:]

#Get ultimate list of all schools and their corresponding school IDs from tab
r0 = requests.get("https://www.tabroom.com/index/results/circuit_chapter.mhtml?circuit_id=6")
t0 = html.fromstring(r0.content)
sn = t0.xpath('//table[@id="sortme"]//a[@class="white medspan wrap"]/text()')

#Strip tab results, and create a dictionary with schools and their corrsponding school IDs
rsn = []
for school in sn:
    rsn.append(school.replace("\n", "").replace("\t", "").rstrip())
su = t0.xpath('//table[@id="sortme"]//a/@href')
schools = dict(zip(rsn, su))
adjschool = [x for x in list(schools.keys()) if targetschool.lower() in x.lower()][0]

#Pull 2016 Results for a specific school
r16 = requests.get("https://www.tabroom.com/index/results/" + schools[adjschool])
t16 = html.fromstring(r16.content)
dn16 = t16.xpath('//div[@class="main"]/h4[text()="Debate Results"]/following-sibling::table[1]//tbody//td/text()')

#Separate the team from the rest of the results and rearrange those results into dictionaries with name, tournament, and record (2016)
results = []
for x in range(0, int(len(dn16)/7)):
    if targetteam[0] in dn16[3 + (7 * x)] and targetteam[1] in dn16[3 + (7 * x)]:
        result = {"Name": dn16[3 + (7 * x)], "Tournament": dn16[7 * x], "Record": dn16[4 + (7 * x)]}
        results.append(result)

print("2016:")
for result in results:
    print(result["Tournament"] + " - " + result["Record"])


#Pull 2015 Results for a specific school
r15 = requests.get("https://www.tabroom.com/index/results/" + schools[adjschool] + "&year=2015")
t15 = html.fromstring(r15.content)
dn15 = t15.xpath('//div[@class="main"]/h4[text()="Debate Results"]/following-sibling::table[1]//tbody//td/text()')

#Separate the team from the rest of the results and rearrange those results into dictionaries with name, tournament, and record (2015)
results2 = []
for x in range(0, int(len(dn15)/7)):
    if targetteam[0].upper() in dn15[3 + (7 * x)] and targetteam[1].upper() in dn15[3 + (7 * x)]:
        result = {"Name": dn15[3 + (7 * x)], "Tournament": dn15[7 * x], "Record": dn15[4 + (7 * x)]}
        results2.append(result)

print("2015:")
for result in results2:
    print(result["Tournament"] + " - " + result["Record"])