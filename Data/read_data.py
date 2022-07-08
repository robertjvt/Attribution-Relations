import os
import re
import sys
import random
random.seed(10)


def read_data(location: str) -> list:
    """Scans through the specified data folder and reads in all the data
    that is stored in the appropriate files.

    :param location: location of the folder
    :return: all combined data
    """
    final_data = []
    temp = []
    id_counter = 0
    id_regex = re.compile(r'[0-9]+')

    if 'VaccinationCorpus' in location:
        # shuffle the file order with a random number
        #directory = sorted(os.scandir(location), key=lambda e: 0.49995030888562586)
        directory = ["cdc-gov_20170701T034626.conll-3",
        "Stop-Mandatory-Vaccination_20170324T022210.conll-3",
        "CIDRAP_20161223T092534.conll-3",
        "LifeSiteNews_20170611T045238.conll-3",
        "Infowars_20160227T205616.conll-3",
        "globalresearch-ca_20170312T001802.conll-3",
        "vernoncoleman-com_20130321T100056.conll-3",
        "Hepatitis-B-Foundation_20160630T014450.conll-3",
        "tripadvisor-com_20150223T054324.conll-3",
        "emergency-cdc-gov_20170616T203204.conll-3",
        "Respectful-Insolence_20170620T075501.conll-3",
        "UPMC-&-Pitt-Health-Sciences-News-Blog_20161107T195115.conll-3",
        "fitfortravel-scot-nhs-uk_20160608T202918.conll-3",
        "mbah-state-ms-us_20161103T062632.conll-3",
        "cdc-gov_20170617T195505.conll-3",
        "greenmedinfo-com_20170702T213636.conll-3",
        "NaturalNews_20170704T132504.conll-3",
        "the-Guardian_20170928T060038.conll-3",
        "Kid-Nurse_20170619T190950.conll-3",
        "sharylattkisson-com_20171001T192931.conll-3",
        "huffingtonpost-com_20170422T005719.conll-3",
        "en-wikipedia-org_20170519T045515.conll-3",
        "NaturalNews_20170628T201245.conll-3",
        "WIRED_20170525T041726.conll-3",
        "Voices-For-Vaccines_20161129T121825.conll-3",
        "HealthyChildren-org_20170803T235658.conll-3",
        "cdc-gov_20170618T093441.conll-3",
        "Modern-Alternative-Health_20170627T011209.conll-3",
        "NaturalNews_20170628T230637.conll-3",
        "Travel-Ready-MD_20161230T060426.conll-3",
        "PolitiFact_20170926T234644.conll-3",
        "huffingtonpost-com_20170918T110744.conll-3",
        "WebMD_20161211T172512.conll-3",
        "POPSUGAR-Moms_20170223T094908.conll-3",
        "Travel-gc-ca_20170612T162447.conll-3",
        "pregnancyforum-co-uk_20160514T164028.conll-3",
        "Heavy-com_20161018T051334.conll-3",
        "vaccinateyourbaby-org_20170705T165639.conll-3",
        "en-wikipedia-org_20170318T104602.conll-3",
        "Respectful-Insolence_20170806T205046.conll-3",
        "Live-Science_20170315T223305.conll-3",
        "patient-info_20161206T035340.conll-3",
        "Nature-News-&-Comment_20170321T211158.conll-3",
        "tmb-ie_20170613T100420.conll-3",
        "nhs-uk_20170628T213437.conll-3",
        "International-Medical-Council-on-Vaccination_20170701T172125.conll-3",
        "justthevax-blogspot-nl_20161107T201500.conll-3",
        "immunize-org_20161124T165410.conll-3",
        "21st-Century-Wire_20170627T181355.conll-3",
        "Veazie-Vet_20170312T000521.conll-3",
        "butterflybirth-com_20170222T111741.conll-3",
        "Ars-Technica_20170629T055731.conll-3",
        "Variety_20170614T212541.conll-3",
        "cid-oxfordjournals-org_20161019T051428.conll-3",
        "NaturalNews_20170707T040258.conll-3",
        "WordReference-Forums_20170118T034336.conll-3",
        "vaccinestoday-eu_20161104T192439.conll-3",
        "World-Health-Organization_20161127T044327.conll-3",
        "nhs-uk_20170704T230508.conll-3",
        "PublicHealth-org_20170623T200727.conll-3",
        "cdc-gov_20170626T170211.conll-3",
        "vaccines-gov_20170627T180812.conll-3",
        "cdc-gov_20170618T093427.conll-3",
        "immunize-ca_20170306T102740.conll-3",
        "NewsComAu_20160212T080640.conll-3",
        "WebMD_20161215T171230.conll-3",
        "NPR-org_20171001T221620.conll-3",
        "vaccinepapers-org_20170929T065440.conll-3",
        "The-People's-Chemist_20170219T051704.conll-3",
        "the-Guardian_20170603T090049.conll-3",
        "en-wikipedia-org_20170702T222036.conll-3",
        "thinktwice-com_20170627T225319.conll-3",
        "fitfortravel-scot-nhs-uk_20160609T200836.conll-3",
        "Skeptical-Raptor_20170628T161832.conll-3",
        "vaccines-gov_20161109T074638.conll-3",
        "Epilepsy-Foundation_20161027T230500.conll-3",
        "nhs-uk_20170705T165550.conll-3",
        "greenmedinfo-com_20170703T045312.conll-3",
        "betterhealth-vic-gov-au_20170706T041705.conll-3",
        "health-gov-on-ca_20170109T215856.conll-3",
        "unicef-org_20161024T164946.conll-3",
        "phac-aspc-gc-ca_20160823T123914.conll-3",
        "Infowars_20170416T154207.conll-3",
        "cdc-gov_20170617T024454.conll-3",
        "Leesburg-Vet-Blog_20170510T163638.conll-3",
        "historyofvaccines-org_20161124T080529.conll-3",
        "nhs-uk_20161127T090556.conll-3",
        "Vaccines-News_20170313T151349.conll-3",
        "NaturalNewsBlogs_20170701T111215.conll-3",
        "fda-gov_20170629T110653.conll-3",
        "fitfortravel-scot-nhs-uk_20160609T200958.conll-3",
        "vaccines-gov_20170627T180818.conll-3",
        "Kid-Nurse_20170627T195033.conll-3",
        "WebMD_20170626T182528.conll-3",
        "Child-Health-Safety_20170626T115833.conll-3",
        "oredigger-net_20160729T150530.conll-3",
        "Stop-Mandatory-Vaccination_20161120T082441.conll-3",
        "patient-info_20161208T092237.conll-3",
        "Newstarget-com_20170301T142751.conll-3",
        "CNN_20170808T234859.conll-3",
        "en-wikipedia-org_20170615T120212.conll-3",
        "Ars-Technica_20171003T014942.conll-3",
        "historyofvaccines-org_20170712T124235.conll-3",
        "Kelly-Brogan-MD_20170813T110455.conll-3",
        "NaturalNews_20161122T084557.conll-3",
        "huffingtonpost-com_20170918T144729.conll-3",
        "dogsnaturallymagazine-com_20160430T211917.conll-3",
        "Activist-Post_20170704T090503.conll-3",
        "dogsnaturallymagazine-com_20170804T052804.conll-3",
        "Gizmodo_20170914T094139.conll-3",
        "WebMD_20160823T183837.conll-3",
        "The-Conversation_20170404T205549.conll-3",
        "NBC-News_20170816T081550.conll-3",
        "CNN_20170928T102949.conll-3",
        "Science-Based-Medicine_20170701T065108.conll-3",
        "Atlas-Monitor_20160703T084322.conll-3",
        "National-Vaccine-Information-Center-(NVIC)_20170701T193111.conll-3",
        "Mayo-Clinic_20170728T184145.conll-3",
        "Science-2-0_20170620T174043.conll-3",
        "influenzareport-com_20161018T081025.conll-3",
        "nhs-uk_20170706T012239.conll-3",
        "patient-info_20161214T134949.conll-3",
        "VaxTruth-org_20170606T065016.conll-3",
        "en-wikipedia-org_20170706T122510.conll-3",
        "fitfortravel-scot-nhs-uk_20160608T230856.conll-3",
        "rivm-nl_20161018T070933.conll-3",
        "fitfortravel-scot-nhs-uk_20160608T231638.conll-3",
        "WebMD_20161222T195704.conll-3",
        "Couples-Resorts-Message-Board_20160822T123023.conll-3",
        "news-nationalgeographic-com_20161231T161535.conll-3",
        "cdc-gov_20170618T203332.conll-3",
        "avn-org-au_20170316T033821.conll-3",
        "cdc-gov_20170629T201906.conll-3",
        "The-EverGreen-Center_20170227T233225.conll-3",
        "World-Health-Organization_20170102T021727.conll-3",
        "cdc-gov_20170618T093430.conll-3",
        "en-wikipedia-org_20170412T054820.conll-3",
        "medlineplus-gov_20170705T195333.conll-3",
        "vaccine-injury-info_20170922T015859.conll-3",
        "yahoo-com_20161107T201934.conll-3",
        "The-Independent_20170915T154519.conll-3",
        "nature-com_20170423T083747.conll-3",
        "cdc-gov_20170617T115003.conll-3",
        "cdc-gov_20170706T111717.conll-3",
        "vaccines-gov_20170627T223546.conll-3",
        "Collective-Evolution_20170926T182201.conll-3",
        "the-Guardian_20160416T111806.conll-3",
        "cdc-gov_20170621T142105.conll-3",
        "fiercepharma-com_20170929T110920.conll-3",
        "vaccines-gov_20170501T023959.conll-3",
        "acsh-org_20170607T114623.conll-3",
        "wonkette-com_20160919T234256.conll-3",
        "thinktwice-com_20170627T191857.conll-3",
        "fitfortravel-nhs-uk_20160812T172501.conll-3",
        "chicagotribune-com_20170918T235148.conll-3",
        "Vaccine-Impact_20160729T094056.conll-3",
        "nhs-uk_20170706T141838.conll-3",
        "nhs-uk_20170705T230324.conll-3",
        "unicef-org_20170623T164121.conll-3",
        "patient-info_20161201T075316.conll-3",
        "WebMD_20160925T143503.conll-3",
        "Natural-Health-365_20170311T150826.conll-3",
        "biology-stackexchange-com_20161125T190915.conll-3",
        "patient-info_20161213T214035.conll-3",
        "mirror_20170321T120113.conll-3",
        "World-Health-Organization_20161126T161524.conll-3",
        "Health-Impact-News_20170428T192431.conll-3",
        "State-of-Health_20160131T151029.conll-3",
        "netmums-com_20160105T011148.conll-3",
        "content-healthaffairs-org_20170210T090820.conll-3",
        "aids-gov_20170513T020021.conll-3",
        "patient-info_20161205T103908.conll-3",
        "Immunisation-Advisory-Centre_20170406T054004.conll-3",
        "info-cmsri-org_20170226T070402.conll-3",
        "NPR-org_20161222T133200.conll-3",
        "SELF_20170611T091338.conll-3",
        "Modern-Alternative-Health_20160113T071212.conll-3",
        "KXAN-com_20171002T213140.conll-3",
        "immunizeforgood-com_20170626T232640.conll-3",
        "Travelfish_20151026T141531.conll-3",
        "greenmedinfo-com_20161214T033718.conll-3",
        "vaccines-gov_20161105T155518.conll-3",
        "immunize-ca_20160924T210421.conll-3",
        "World-Health-Organization_20160503T120356.conll-3",
        "cdc-gov_20170703T010627.conll-3",
        "usnews-com_20161018T172826.conll-3",
        "The-Cat-Site_20161128T023535.conll-3",
        "World-Health-Organization_20170419T052836.conll-3",
        "Daily-Intelligencer_20160903T110638.conll-3",
        "cdc-gov_20170614T145809.conll-3",
        "LDI_20150623T130008.conll-3",
        "Backyard-Secret-Exposed_20161021T055227.conll-3",
        "who-int_20161208T191344.conll-3",
        "Parents_20170705T132137.conll-3",
        "ncbi-nlm-nih-gov_20160228T014103.conll-3",
        "vaccines-gov_20170611T191047.conll-3",
        "vaccines-gov_20161016T063224.conll-3",
        "cdc-gov_20170701T133819.conll-3",
        "Petful_20170310T005844.conll-3",
        "thehealthyhomeeconomist-com_20170810T004952.conll-3",
        "virology-ws_20170623T174458.conll-3",
        "Global-News_20161110T054038.conll-3",
        "nhs-uk_20170705T203045.conll-3",
        "The-Independent_20170606T163405.conll-3",
        "GGD-Amsterdam_20160921T061812.conll-3",
        "mom-me_20150906T191238.conll-3",
        "WebMD_20170628T103153.conll-3",
        "Fox-News_20161029T114432.conll-3",
        "Truth4Dogs_20161026T182655.conll-3",
        "who-int_20170327T043644.conll-3",
        "vaccines-gov_20170627T175244.conll-3",
        "fodors-com_20161027T194550.conll-3",
        "nhs-uk_20170706T161341.conll-3",
        "en-wikipedia-org_20170701T015555.conll-3",
        "hepb-org_20160629T112215.conll-3",
        "Voices-For-Vaccines_20170228T194925.conll-3",
        "vaccineinformation-org_20170612T112221.conll-3",
        "nytimes-com_20161229T124138.conll-3",
        "vaccines-gov_20170114T204931.conll-3",
        "@berkeleywellness_20170709T195101.conll-3",
        "fitfortravel-nhs-uk_20160812T212733.conll-3",
        "ThinkProgress_20160723T110700.conll-3",
        "nhs-uk_20170704T031554.conll-3",
        "NaturalNews_20170606T044813.conll-3",
        "patient-info_20161107T030600.conll-3",
        "healthtalk-org_20161031T152854.conll-3",
        "ABC-News_20170511T203024.conll-3",
        "nation19-com_20170327T045532.conll-3",
        "VacTruth-com_20170326T020022.conll-3",
        "HealthyChildren-org_20151012T214316.conll-3",
        "fitfortravel-scot-nhs-uk_20160609T202116.conll-3",
        "petmd-com_20170209T130913.conll-3",
        "Washington-Post_20170826T112301.conll-3",
        "patient-info_20161217T210240.conll-3",
        "Scientific-American_20170506T132335.conll-3",
        "World-Health-Organization_20170403T184820.conll-3",
        "NY-Daily-News_20160704T092017.conll-3",
        "phac-aspc-gc-ca_20160810T020655.conll-3",
        "World-Economic-Forum_20160927T220244.conll-3",
        "Global-Freedom-Movement_20170830T214655.conll-3",
        "Carrington_20170630T081323.conll-3",
        "vaccinateyourbaby-org_20161105T032915.conll-3",
        "vk-ovg-ox-ac-uk_20170821T010049.conll-3",
        "health-ny-gov_20170701T054023.conll-3",
        "immunize-ca_20160804T232639.conll-3",
        "National-Vaccine-Information-Center-(NVIC)_20170616T025538.conll-3",
        "tripadvisor-com-au_20140823T095105.conll-3",
        "euro-who-int_20161216T112353.conll-3",
        "National-Vaccine-Information-Center-(NVIC)_20170615T175941.conll-3",
        "The-Forum-at-Harvard-T--H--Chan-School-of-Public-Health_20150926T091541.conll-3",
        "nhs-uk_20170705T165547.conll-3",
        "immunize-org_20170528T115030.conll-3",
        "PBS-NewsHour_20161202T134302.conll-3",
        "vk-ovg-ox-ac-uk_20170912T071447.conll-3",
        "Science-_-AAAS_20170707T030050.conll-3",
        "patient-info_20161209T104048.conll-3",
        "phac-aspc-gc-ca_20160825T001220.conll-3",
        "Science-News_20170517T164904.conll-3",
        "latimes-com_20170206T032149.conll-3",
        "nhs-uk_20170705T182412.conll-3",
        "The-West-Australian_20170608T145504.conll-3",
        "Scientific-American_20170112T025035.conll-3",
        "California-Healthline_20150817T012959.conll-3",
        "Whattoexpect_20161206T224915.conll-3",
        "BBC-News_20161119T015125.conll-3",
        "healthycanadians-gc-ca_20161203T154835.conll-3",
        "patient-info_20170211T092911.conll-3",
        "Banning-Beaumont-CA-Patch_20150812T082915.conll-3",
        "immunise-health-gov-au_20170626T104650.conll-3",
        "hepb-org_20160713T190256.conll-3",
        "fitfortravel-nhs-uk_20160812T165007.conll-3",
        "International-Medical-Council-on-Vaccination_20170308T114510.conll-3",
        "nhs-uk_20170704T190040.conll-3",
        "Reuters_20161107T200904.conll-3",
        "huffingtonpost-com_20161221T170356.conll-3",
        "drsuzanne-net_20170606T042830.conll-3",
        "vaccines-gov_20161018T021014.conll-3",
        "blogs-cdc-gov_20170616T233823.conll-3",
        "National-Vaccine-Information-Center-(NVIC)_20170625T020431.conll-3",
        "POLITICO_20170925T004222.conll-3",
        "nytimes-com_20170309T113837.conll-3",
        "NPR-org_20170313T074645.conll-3",
        "latimes-com_20170628T014330.conll-3",
        "NaturalNews_20170706T012448.conll-3",
        "uptodate-com_20161125T164528.conll-3",
        "AGE-OF-AUTISM_20170620T044415.conll-3",
        "nap-edu_20160617T022642.conll-3",
        "greenmedinfo-com_20160402T131018.conll-3",
        "Science-News-for-Students_20160715T223017.conll-3",
        "vaccineinformation-org_20170611T231651.conll-3",
        "cdc-gov_20170521T155133.conll-3",
        "jabs-org-uk_20160617T081707.conll-3",
        "Church-Law-&-Tax_20170707T234627.conll-3"]
    else:
        # keep the directory sorted
        directory = sorted(os.scandir(location), key=lambda e: e.name)

    for entry in directory:
        file_data = []
        if 'VaccinationCorpus' not in location:
            if entry.name.endswith('.conll') or entry.name.endswith('features') or entry.name.endswith('.conll-3') and entry.is_file():
                with open(entry.path, encoding='utf8') as file:
                    # Create a dictionary of all AR id's and give it a new unique value
                    in_file = file.readlines()
                    in_file.append('\n')
                    for line in in_file:
                        if line == '\n':
                            file_data.append(temp)
                            temp = []
                        else:
                            temp.append(line.rstrip().split('\t'))
                    id_dict, id_counter = create_id_dict(file_data, id_counter)

                    # Convert AR id's to be unique over all files
                    for line in in_file:
                        if line == '\n':
                            final_data.append(temp)
                            temp = []
                        else:
                            line = line.rstrip().split('\t')
                            if re.findall(id_regex, line[-1]):
                                for found_id in re.findall(id_regex, line[-1]):
                                    repl_id = r'(?<![0-9])' + found_id + '(?![0-9])'
                                    line[-1] = re.sub(repl_id, str(id_dict[found_id]), line[-1])
                            temp.append(line)
        else:
            if entry[-8:] == '.conll-3':
                loc = "../Data/VaccinationCorpus/" + entry
                with open(loc, encoding='utf8') as file:
                    # Create a dictionary of all AR id's and give it a new unique value
                    in_file = file.readlines()
                    in_file.append('\n')
                    for line in in_file:
                        if line == '\n':
                            file_data.append(temp)
                            temp = []
                        else:
                            temp.append(line.rstrip().split('\t'))
                    id_dict, id_counter = create_id_dict(file_data, id_counter)

                    # Convert AR id's to be unique over all files
                    for line in in_file:
                        if line == '\n':
                            final_data.append(temp)
                            temp = []
                        else:
                            line = line.rstrip().split('\t')
                            if re.findall(id_regex, line[-1]):
                                for found_id in re.findall(id_regex, line[-1]):
                                    repl_id = r'(?<![0-9])' + found_id + '(?![0-9])'
                                    line[-1] = re.sub(repl_id, str(id_dict[found_id]), line[-1])
                            temp.append(line)

    # for i in final_data:
    #     for j in i:
    #         print(j)

    return final_data


def create_id_dict(file_data, id_counter):
    """Creates a dictionary to give each AR ID (key) a new unique value (value).

    :param: file_data: the data in one file
    :param: id_counter: a counter that increments over all files
    :return: a dictionary with unique ID for each AR ID
    """
    id_dict = {}
    id_regex = re.compile(r'[0-9]+')
    for sentence in file_data:
        for token in sentence:
            if re.findall(id_regex, token[-1]):
                for found_id in re.findall(id_regex, token[-1]):
                    if found_id not in id_dict:
                        id_dict[found_id] = id_counter
                        id_counter += 1
    return id_dict, id_counter


def extract_tokens_labels(all_data: list, argv: str) -> list:
    """Extracts all tokens and corresponding labels per token.

    :param all_data: data from all files
    :param argv: name of the dataset folder
    :return: sentences of tuples of a token and its label(s)
    """
    # Find the tokens: (?:[A-Za-z-[0-9])+
    # Find blanco tokens: (?:B-|I-)(?:CUE|CONTENT|SOURCE)
    token_re = re.compile(r'(?:B|I)-[A-Z]+-[0-9]+')
    tokens_labels = []
    for sentence in all_data:
        temp = []
        for token in sentence:
            if 'PARC3.0' in argv or 'POLNEAR' in argv:
                if '_' in token[-1]:
                    label = token[-1].replace('_', '').split()
                    temp.append((token[8], label))
                else:
                    temp.append((token[8], []))
            elif 'VaccinationCorpus' in argv:
                label = re.findall(token_re, token[-1])
                temp.append((token[3], label))
        tokens_labels.append(temp)
    return tokens_labels


def structure_data(tokens_labels: list, argv: str) -> list:
    """Structure the data so that a model can be trained on it. This means
    that each token can only have 1 label and tokens with no label are labeled
    as 'O'.

    :param tokens_labels: tokens and corresponding labels
    :param argv: name of the dataset folder
    :return: structured data
    """
    clean_data = []
    nested_regex = re.compile(r'[A-Za-z\-]+-NE-[0-9]+')
    label_regex = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    id_regex = re.compile(r'[0-9]+')

    if 'PARC3.0' in argv or 'POLNEAR' in argv:
        for sentence in tokens_labels:
            temp = []
            for label_tokens in sentence:
                tokens = label_tokens[1]
                filtered_token = [i for i in tokens if not nested_regex.match(i)]
                if filtered_token != []:
                    match = re.match(label_regex, filtered_token[0]) or 'O'
                    if match != 'O':
                        match = match[0] + '-' + str(id_regex.search(filtered_token[0])[0])
                    temp.append((label_tokens[0], match))
                else:
                    temp.append((label_tokens[0], 'O'))
            clean_data.append(temp)

    elif 'VaccinationCorpus' in argv:
        for sentence in tokens_labels:
            first_token = ''
            temp = []
            for i in sentence:
                if first_token == '':
                    if i[1] != []:
                        if len(first_token) > 1:
                            first_token = i[1][0]
                        else:
                            first_token = i[1]
                if i[1] != [] and i[1][0][-2:] == first_token[0][-2:]:
                    match = i[1][0]
                    if match is not None:
                        temp.append((i[0], match))
                    else:
                        temp.append((i[0], 'O'))
                else:
                    temp.append((i[0], 'O'))
            clean_data.append(temp)

    return clean_data


def remove_multi_ars(data):
    ar_id = re.compile(r'[0-9]+')
    label_regex = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    ar_sent_count = {}
    removed_data = []
    for sentence in data:
        found_ids = []
        for token_label in sentence:
            if token_label[1] != 'O':
                label_id = ar_id.search(token_label[1])[0]
                if label_id not in found_ids:
                    found_ids.append(label_id)
        for id in found_ids:
            if id not in ar_sent_count:
                ar_sent_count[id] = 1
            else:
                ar_sent_count[id] += 1

    for sentence in data:
        temp = []
        for token_label in sentence:
            if token_label[1] != 'O':
                clean_label = label_regex.search(token_label[1])[0]
                label_id = ar_id.search(token_label[1])[0]
                if ar_sent_count[label_id] > 3:
                    temp.append((token_label[0], 'O'))
                else:
                    temp.append((token_label[0], clean_label))
            else:
                temp.append((token_label[0], 'O'))
        removed_data.append(temp)

    # for i, sent in enumerate(data):
    #     print(data[i])
    #     print(removed_data[i])
    return removed_data


def main(argv: str) -> list:
    # parc loc: "../Data/PARC3.0/PARC_tab_format/dev"
    # polnear loc: "../Data/POLNEAR_enriched/dev"
    # vaccination loc: "../Data/VaccinationCorpus/testing"

    all_data = read_data(argv)
    tokens_labels = extract_tokens_labels(all_data, argv)
    clean_data = structure_data(tokens_labels, argv)
    removed_data = remove_multi_ars(clean_data)

    return removed_data



if __name__ == "__main__":
    main(sys.argv[1])
