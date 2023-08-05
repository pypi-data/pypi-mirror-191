from dependencies import *
from dict_api import fetch_dictionary
from dict_api import fetch_snapshot
from dict_api import write_to_influxdb
print('hello')
class DataCenter:
    def __init__(self,inputradarID,timeepo5min):
        print('hello')
        self.inputradarID= inputradarID
        print(self.inputradarID)
        self.timeepo5min=timeepo5min
        print(datetime.fromtimestamp(int(self.timeepo5min)))
        self.influx_url = "https://us-central1-1.gcp.cloud2.influxdata.com"
        self.influx_token = "1YczpUQeWsc9zyLG8WYhMptyPbyETwkrfSEtDkXY9XU3f2N3fnyDwPr6u9ER4plyylGi4k0UEpb4rkqRQgZflA=="
        self.org = "Data"
        self.bucket = "Datacenter"
        self.context = ssl.SSLContext()
        self.context.load_verify_locations('/home/halsakka/PythonHas/DataCenterHub/DataCenterHubCA.pem')
        self.req='https://localhost:8444/api/dictionary?prefix=' + self.inputradarID
        self.root_certificate='/home/halsakka/PythonHas/DataCenterHub/DataCenterHubCA.pem'
        #print('check')
        try:
            tt=fetch_dictionary(self.req, self.root_certificate)
            for group in zip_longest(*[iter(tt)]*200,fillvalue=None):
                aa=''
                SysState=[]
                SubSyst=[]
                ShortName=[]
                group = [x for x in group if x is not None]
                for x in group:
                    SysState.append(x['state'])
                    SubSyst.extend(x['subsystems'])
                    ShortName.append(x['shortname'])
                    aa=x['state']+','+aa

                reqe='https://localhost:8444/api/snapshot?prefix=' + self.inputradarID+ '&timestamp=' + self.timeepo5min + '000' + '&states=' + aa
                
                data_dict = dict(zip(SysState, zip(SubSyst, ShortName)))

                SubSyst_o=[]
                ShortName_o=[]
                SysState_o=[]
                StateValue=[]
                radarID,radarBand,bb,country=fetch_snapshot(reqe,self.root_certificate)
                for value in bb:
                    statename=value['statename']
                    if statename in data_dict:
                        SysState_o.append(statename)
                        SubSyst_o.append(data_dict[statename][0])
                        ShortName_o.append(data_dict[statename][1])
                        StateValue.append(value['value'])
                #print(np.unique(SubSyst_o))
                write_to_influxdb(self.inputradarID,self.timeepo5min,radarBand,radarID,SubSyst_o,ShortName_o,StateValue,self.influx_url,self.influx_token,self.org,self.bucket,bb,country)

        except Exception as err:
            print(f'Other error occurred: {err}')
if __name__=="__main__":
    #data_run=DataCenter('238aus20',str(int(time.time())))
    data_run=DataCenter(sys.argv[1],sys.argv[2])
