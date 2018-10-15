"""*************************************************************************************************
This document contains examples related to XML, CSV and DB

====DSC XML Process
code in this section is for illustrative purpose:
dscxmlpeer2csv(dsc_config_xml_name,peer_info_csv_name)#use root and layer
dscxml_ip_host(dsc_config_xml_name,ip_host_csv_name)#use root.iter
def dscxml_to_test_peer(dsc_config_xml_name)#use root.iter

====XML
IT_XMLDBCSV_XML2CSV_findall(XML_filename,CSV_filename)#use tree.findall
IT_XMLDBCSV_SOAP2XML(SURL,SENV,filename)

====DB
IT_XMLDBCSV_DB2CSV(host,port,user,pwd,db,sql,outputfile)

====CSV
IT_XMLDBCSV_csv_with_header_2_ordered_dict(csv_file)
IT_XMLDBCSV_csv_with_no_header_2_list(CSV_filename)


20181014 Wind

*************************************************************************************************"""

"""*************************************************************************************************
dscxmlpeer2csv read DSC xml config and summaris all peer info parameter into csv file
root and layer is used as method
<Configuration xmlns="http://www.syniverse.com/diameter-server">
  <Network>
    <Peers>	
      <Peer display_name="CMI-Riley-DRA" name="aaa://dra01.dra.ipx.cmi.3gppnetwork.org:3868;transport=sctp" realm="dra.ipx.cmi.3gppnetwork.org" remote_ip="223.118.35.97,223.118.35.105" remote_pip="" attempt_connect="true" allowedHosts="*" allowedRealms="*" maxActive="1" masquerade="false" removeRR="false" security_ref="securityData_dscadm" profile="default-profile" peer_type="Third-party-peer" peer_mtu="1500" throttling_action="drop">
        <PeerConnections>#<-layer.tag  '{http://www.syniverse.com/diameter-server}PeerConnections'
          #layer.attrib                                                      layer.attrib    layer.attrib                            
          <PeerConnection name="aaa://dra01.dra.ipx.cmi.3gppnetwork.org:3868;transport=sctp" rating="1" local_port_range="17174"/>
        </PeerConnections>
        <PeerParameters>
          <MessageTimeOut value="10000"/>
          <MaxInboundStreams value="17"/>
          <MaxOutboundStreams value="17"/>
        </PeerParameters>
      </Peer>
Wind 20181014
*************************************************************************************************"""

def dscxmlpeer2csv(dsc_config_xml_name,peer_info_csv_name):
	import xml.etree.ElementTree as ET
	import copy
	import os
	tree = ET.parse(dsc_config_xml_name)
	root = tree.getroot()
	#print(root.tag)
	record={}
	result_list=[]
	keys=['display_name','name','realm','remote_ip','remote_pip','attempt_connect','maxActive',\
	'disabled','peer_test_mode','peer_mtu','local_port_range_1','local_port_range_2',\
	'local_port_range_3','local_port_range_4','local_port_range_5','local_port_range_6','local_port_range_7',\
	'local_port_range_8','MaxInboundStreams','MaxOutboundStreams']
	
	for layer1 in root:
	
		if layer1.tag=='{http://www.syniverse.com/diameter-server}Network':
			for layer2 in layer1:
				if layer2.tag=='{http://www.syniverse.com/diameter-server}Peers':
					for layer3 in layer2:
						if layer3.tag=='{http://www.syniverse.com/diameter-server}Peer':
						#all code layer above can be condensed into line masked below:
						#for layer3 in root.iter('{http://www.syniverse.com/diameter-server}Peer'):
							
							for key in keys:#add empty value to each key so they can be correctly printed in CSV even if the parameter not exist in config
								record[key]=''
							#parameters which must exist
							record['display_name']=layer3.attrib['display_name']
							record['name']=layer3.attrib['name']
							record['realm']=layer3.attrib['realm']
							record['remote_ip']=layer3.attrib['remote_ip']
							record['remote_pip']=layer3.attrib['remote_pip']
							record['attempt_connect']=layer3.attrib['attempt_connect']
							record['maxActive']=layer3.attrib['maxActive']
							#optional parameters
							try:
								record['disabled']=layer3.attrib['disabled']
							except KeyError:
								record['disabled']='Null'
							try:
								record['peer_test_mode']=layer3.attrib['peer_test_mode']
							except KeyError:
								record['peer_test_mode']='Null'
							try:
								record['peer_mtu']=layer3.attrib['peer_mtu']
							except KeyError:
								record['peer_mtu']='Null'
	
							for layer4 in layer3:#Peerconnections or PeerParameters
								if layer4.tag=='{http://www.syniverse.com/diameter-server}PeerParameters':
									for layer5 in layer4:#Inbound or Outbound
										if layer5.tag=='{http://www.syniverse.com/diameter-server}MaxInboundStreams':
											record['MaxInboundStreams']=layer5.attrib['value']
										if layer5.tag=='{http://www.syniverse.com/diameter-server}MaxOutboundStreams':
											record['MaxOutboundStreams']=layer5.attrib['value']
							
								if layer4.tag=='{http://www.syniverse.com/diameter-server}PeerConnections':
									local_port_range_index=0
									for layer5 in layer4:#Peerconnection
										local_port_range_index=local_port_range_index+1
										id='local_port_range_'+str(local_port_range_index)
										#print(layer5.tag)
										#print(layer5.attrib)
										try:
											record[id]=layer5.attrib['local_port_range']
										except KeyError:
											break
							result_list.append(copy.deepcopy(record))

	import csv
	location_file=os.getcwd()+r'\file\xml\{0}'.format(peer_info_csv_name)
	#print(location_file)
	with open(location_file, 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		string=[]
		for key in keys:
			string.append(key)
		spamwriter.writerow(string)
		for row in result_list:
			string=[]
			for key in keys:
				string.append(row[key])
			spamwriter.writerow(string)

"""*************************************************************************************************
dscxml_ip_host read DSC xml config and summaris all ip host parameter into csv file
root.iter is used to locate the items
<Configuration xmlns="http://www.syniverse.com/diameter-server">
  <Network>
    <Peers>																		   #attrib                               attrib
      <Peer display_name="Syn-Chicago-DRA" name="aaa://dp01-chi.syniverse.com:3868;transport=sctp" realm="syniverse.com" remote_ip="205.174.191.6,205.174.191.22" remote_pip="" attempt_connect="false" allowedHosts="*" allowedRealms="*" maxActive="10" masquerade="false" removeRR="false" security_ref="securityData_dscadm" profile="default-profile" disabled="false" peer_test_mode="false" peer_type="Syniverse-peer" peer_mtu="1500" throttling_action="drop">
        <PeerConnections>
          <PeerConnection name="aaa://dp01-chi.syniverse.com:3868;transport=sctp" rating="1" max_connection="10"/>
        </PeerConnections>
        <PeerParameters>
          <MessageTimeOut value="10000"/>
        </PeerParameters>
      </Peer>
Wind 20181014
*************************************************************************************************"""
def dscxml_ip_host(dsc_config_xml_name,ip_host_csv_name):
	record={}
	tree = ET.parse(dsc_config_xml_name)
	root = tree.getroot()
	content=''
	for item in root.iter('{http://www.syniverse.com/diameter-server}Peer'):
		ips=item.attrib['remote_ip']
		display_name=item.attrib['display_name']
		ip_list=ips.split(",")
		for i in ip_list:
			content=content+i+","+display_name+'\n'
	with open(ip_host_csv_name,'w') as file_object:
		file_object.write(content)

"""*************************************************************************************************
dscxml_to_test_peer read DSC xml config and put all peername with test mode=true in to a string 
segmented with "|"
into csv file
root.iter is used to locate the items
Wind 20181014
*************************************************************************************************"""		
def dscxml_to_test_peer(dsc_config_xml_name):
	test_peers=''
	record={}
	tree = ET.parse(dsc_config_xml_name)
	root = tree.getroot()
	content=''
	for item in root.iter('{http://www.syniverse.com/diameter-server}Peer'):
		try:
			test_mode=item.attrib['peer_test_mode']
		except:
			test_mode="None"

		peer_name=item.attrib['name'][6:].split(";")[0].split(":")[0]
		if test_mode == "true":
			test_peers=test_peers+peer_name+"|"
	test_peers=test_peers[:-1]#remove the last "|" in the string

	return(test_peers)	
		
#test script
#filename='HKG201808130946.xml'
#dsc_config_xml_name=os.getcwd()+r'\file\xml\{0}'.format(filename)
#dscxml_ip_host(dsc_config_xml_name,'HKG_ip_host.csv'')

"""====XML***************************************************************************************"""
"""*************************************************************************************************
IT_XMLDBCSV_XML2CSV_findall use tree.findall to find content in XML and put it into CSV
into csv file
<listCaches>
<listCache>mmec01.mmegi8000.mme.epc.mnc000.mcc454.3gppnetwork.org</listCache>
<listCache>mmec02.mmegi8000.mme.epc.mnc000.mcc454.3gppnetwork.org</listCache>
<listCache>mmec03.mmegi8000.mme.epc.mnc000.mcc454.3gppnetwork.org</listCache>
<listCache>mmec04.mmegi8000.mme.epc.mnc000.mcc454.3gppnetwork.org</listCache>
<listCacheName>LIST_CSL_MME</listCacheName>
</listCaches>
Wind 20181014
*************************************************************************************************"""

def IT_XMLDBCSV_XML2CSV_findall(XML_filename,CSV_filename):
	from xml.etree import ElementTree as ET
	import csv

	tree=ET.parse(XML_filename)
	listCaches= tree.findall('.//listCaches')
	with open(CSV_filename, 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		L=['LISTNAME']
		spamwriter.writerow(L)
		for row in listCaches:
			string=[]
			for item in row:
				if item.tag=="listCacheName":
					string.insert(0,item.text) 
				else:
					string.append(item.text)
			spamwriter.writerow(string)

"""*************************************************************************************************
IT_XMLDBCSV_SOAP2XML get soap feedback and put it into xml file

Wind 20181014
*************************************************************************************************"""
def IT_XMLDBCSV_SOAP2XML(SURL,SENV,filename):
	import requests
	headers = {'Host': ''}
	headers = {'content-type': 'text/xml'}
	headers = {'soapAction': ''}
	response = requests.post(SURL,data=SENV,headers=headers)
	with open(filename, 'w') as file_object:
		file_object.write(response.text)
	return response
	
SOAP_QueryAllListCaches = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://ws.soap.dsc.syniverse.com/"><soapenv:Header/><soapenv:Body><ws:dscAllListCachesClient/></soapenv:Body></soapenv:Envelope>"""
url="http://10.162.28.186:8080/DSC_SOAP/query?"
#print(SOAP2XML(url,SOAP_QueryAllListCaches,"SOAP2XML_OUTPUT.xml"))

"""*************************************************************************************************
IT_XMLDBCSV_DB2CSV read mysql DB into a list of dictionary and put content into csv file

Wind 20181014
*************************************************************************************************"""

def IT_XMLDBCSV_DB2CSV(host,port,user,pwd,db,sql,outputfile):
	import pymysql.cursors,traceback
	namelist=[] 
	#连接配置信息
	config = {
		'host':host,
		'port':port,
		'user':user,
		'password':pwd,
		'db':db,
		'charset':'utf8mb4',
		'cursorclass':pymysql.cursors.DictCursor,
		}
	# 创建连接
	connection = pymysql.connect(**config)

# 执行sql语句
	try:
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = sql
			cursor.execute(sql)
			# 获取查询结果
			results = cursor.fetchall()
			#没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
		connection.close()
	except:
		traceback.print_exc()
		results=""
		return(results)

	import csv

	with open(outputfile, 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		string=[]
		for keys in results[1]:
			string.append(keys)
		spamwriter.writerow(string)
		for row in results:
			string=[]
			for key in results[1]:
				string.append(row[key])
			spamwriter.writerow(string)
	return(results)

#print(DB2CSV('da3p-gen-opx-ctd001.syniverse.com',3306,'dssossreadonly','DsOs_4eaD','dss_oss',"""SELECT id, ssid, hub, hubpolicy, hubstatus FROM hubinfo;""",'.\\DB2CSV_output.csv'))

"""====CSV***************************************************************************************"""


"""*************************************************************************************************
csv_with_header_2_dict transfer CSV file with hearder line into dictionary list

Wind 20181014
*************************************************************************************************"""
#transfer CSV file with hearder into dictionary list
def IT_XMLDBCSV_csv_with_header_2_ordered_dict(csv_file):
	import csv
	new_dict = {}
	with open(csv_file, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		fieldnames = next(reader)
		reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
		new_dict = [row for row in reader]
	return new_dict

print(csv_with_header_2_ordered_dict('DB2CSV_output.csv'))

"""*************************************************************************************************
csv_with_no_header_2_list transfer CSV file with no hearder line into list

Wind 20181014
*************************************************************************************************"""
def IT_XMLDBCSV_csv_with_no_header_2_list(CSV_filename):
	import csv
	LIST=[]
	with open(CSV_filename) as f:
		reader =csv.reader(f)
		for row in reader:
			LIST.append(row)
	return(LIST)
