import pymysql
import time
import numpy as np

DAYS = 2
DATABASE = 'rqalpha'


class ConnManage:
    def __init__(self, database):
        self._time_interval = 60 * 5  # 5 min
        self._start_time = time.time()
        self._host = 'localhost'
        self._user = 'root'
        self._passwd = 'asdf..12'
        self._database = database
        self._conn = self._create_conn()

    def _get_conn(self):
        if time.time() - self._start_time > self._time_interval:
            self._conn.close()
            self._conn = self._create_conn()
            self._start_time = time.time()
        return self._conn

    def exec_sql(self, sql):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def query_sql(self, sql):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def _create_conn(self):
        return pymysql.connect(host=self._host, user=self._user, password=self._passwd, database=self._database)


conn_manager = ConnManage(DATABASE)


def cal_return(code, days):
    sql = "select * from get_price where code = '%s' order by trade_date asc" % code
    query_result = conn_manager.query_sql(sql)
    if len(query_result) == 0:
        print('code: %s select result is null' % code)
        return
    close_p = []
    trade_date_list = []
    for items in query_result:
        close_p.append(items[4])
        trade_date_list.append(items[9])
    close_p = np.array(close_p, dtype=np.float32)
    trade_date_list = trade_date_list[days:]
    returns = close_p[days:] / close_p[:-days]
    for i, trade_date in enumerate(trade_date_list):
        ret = returns[i]
        sql = "insert into pre_two_day_returns (close_return, code, trade_date) values ({:.10f}, '{}', '{}')".format(
            ret, code, trade_date)
        conn_manager.exec_sql(sql)


if __name__ == '__main__':
    all_code = '002450.XSHE,600807.XSHG,000878.XSHE,300097.XSHE,300366.XSHE,600108.XSHG,600370.XSHG,601155.XSHG,000782.XSHE,600160.XSHG,002364.XSHE,300178.XSHE,601012.XSHG,603788.XSHG,600877.XSHG,603725.XSHG,300588.XSHE,002449.XSHE,600718.XSHG,600139.XSHG,601811.XSHG,300064.XSHE,601788.XSHG,002312.XSHE,300671.XSHE,300055.XSHE,600563.XSHG,601200.XSHG,002415.XSHE,600804.XSHG,300587.XSHE,600267.XSHG,000090.XSHE,300265.XSHE,603909.XSHG,002646.XSHE,300347.XSHE,300227.XSHE,600302.XSHG,603938.XSHG,002262.XSHE,300063.XSHE,600023.XSHG,002156.XSHE,002725.XSHE,600127.XSHG,300045.XSHE,601018.XSHG,600995.XSHG,600809.XSHG,002828.XSHE,600513.XSHG,300082.XSHE,000611.XSHE,600857.XSHG,600249.XSHG,300051.XSHE,000970.XSHE,002171.XSHE,002623.XSHE,002556.XSHE,603300.XSHG,002634.XSHE,300308.XSHE,600520.XSHG,000751.XSHE,601968.XSHG,600648.XSHG,600401.XSHG,600368.XSHG,002369.XSHE,601633.XSHG,603677.XSHG,601238.XSHG,002431.XSHE,603179.XSHG,300583.XSHE,000524.XSHE,603838.XSHG,603197.XSHG,002452.XSHE,000812.XSHE,000780.XSHE,600601.XSHG,300410.XSHE,600027.XSHG,300589.XSHE,000596.XSHE,000910.XSHE,600029.XSHG,300439.XSHE,002082.XSHE,300058.XSHE,000529.XSHE,601098.XSHG,600640.XSHG,002389.XSHE,002306.XSHE,002573.XSHE,603169.XSHG,600717.XSHG,000572.XSHE,002281.XSHE,002295.XSHE,300641.XSHE,600066.XSHG,600081.XSHG,002347.XSHE,000663.XSHE,601689.XSHG,000850.XSHE,600624.XSHG,002682.XSHE,002802.XSHE,600530.XSHG,002635.XSHE,300295.XSHE,300368.XSHE,002098.XSHE,600392.XSHG,300689.XSHE,600561.XSHG,002175.XSHE,002418.XSHE,002024.XSHE,300307.XSHE,300096.XSHE,600155.XSHG,600179.XSHG,002031.XSHE,600896.XSHG,300212.XSHE,002859.XSHE,300672.XSHE,601519.XSHG,603817.XSHG,600277.XSHG,603226.XSHG,002166.XSHE,002361.XSHE,000554.XSHE,002530.XSHE,603899.XSHG,300258.XSHE,002523.XSHE,600617.XSHG,600719.XSHG,600356.XSHG,600225.XSHG,600698.XSHG,002715.XSHE,300553.XSHE,300434.XSHE,603328.XSHG,603976.XSHG,000656.XSHE,002630.XSHE,600986.XSHG,002671.XSHE,300148.XSHE,603887.XSHG,002001.XSHE,600059.XSHG,600982.XSHG,002029.XSHE,000550.XSHE,000043.XSHE,002518.XSHE,600262.XSHG,600676.XSHG,002601.XSHE,300050.XSHE,600420.XSHG,002305.XSHE,600606.XSHG,600789.XSHG,300489.XSHE,002337.XSHE,002652.XSHE,600106.XSHG,002789.XSHE,002097.XSHE,002487.XSHE,000783.XSHE,002595.XSHE,600512.XSHG,603015.XSHG,600628.XSHG,300288.XSHE,600091.XSHG,603993.XSHG,603399.XSHG,603006.XSHG,002459.XSHE,601006.XSHG,300418.XSHE,002867.XSHE,000564.XSHE,300114.XSHE,300121.XSHE,002872.XSHE,002763.XSHE,002357.XSHE,300427.XSHE,002741.XSHE,600888.XSHG,601718.XSHG,300475.XSHE,002670.XSHE,300241.XSHE,002413.XSHE,600803.XSHG,300416.XSHE,600270.XSHG,000068.XSHE,300373.XSHE,002365.XSHE,000422.XSHE,300059.XSHE,000543.XSHE,600891.XSHG,002557.XSHE,600575.XSHG,000723.XSHE,000802.XSHE,000887.XSHE,002245.XSHE,601169.XSHG,300279.XSHE,300600.XSHE,002717.XSHE,000736.XSHE,603958.XSHG,601158.XSHG,000821.XSHE,600408.XSHG,300620.XSHE,002531.XSHE,300400.XSHE,000534.XSHE,600130.XSHG,600822.XSHG,300490.XSHE,603960.XSHG,300040.XSHE,601607.XSHG,300562.XSHE,300262.XSHE,300111.XSHE,300309.XSHE,603758.XSHG,002411.XSHE,002683.XSHE,002506.XSHE,000948.XSHE,601890.XSHG,600242.XSHG,600722.XSHG,600163.XSHG,002497.XSHE,000612.XSHE,600036.XSHG,600707.XSHG,603081.XSHG,603377.XSHG,603803.XSHG,000681.XSHE,002469.XSHE,002021.XSHE,300143.XSHE,300570.XSHE,600371.XSHG,300090.XSHE,600118.XSHG,600720.XSHG,600114.XSHG,300398.XSHE,600279.XSHG,002137.XSHE,000401.XSHE,300115.XSHE,600550.XSHG,002130.XSHE,002416.XSHE,601579.XSHG,300302.XSHE,603003.XSHG,000875.XSHE,600095.XSHG,000659.XSHE,603040.XSHG,600604.XSHG,603585.XSHG,002169.XSHE,600769.XSHG,600428.XSHG,600506.XSHG,300563.XSHE,000967.XSHE,000050.XSHE,603118.XSHG,600433.XSHG,600336.XSHG,600466.XSHG,603701.XSHG,000576.XSHE,600548.XSHG,002659.XSHE,000420.XSHE,002092.XSHE,600053.XSHG,600272.XSHG,601113.XSHG,002320.XSHE,600837.XSHG,002526.XSHE,300134.XSHE,000017.XSHE,000607.XSHE,600339.XSHG,002371.XSHE,300647.XSHE,002247.XSHE,600830.XSHG,600694.XSHG,002723.XSHE,300415.XSHE,300444.XSHE,002658.XSHE,600010.XSHG,002153.XSHE,600638.XSHG,603903.XSHG,002607.XSHE,002821.XSHE,600169.XSHG,000027.XSHE,002363.XSHE,000935.XSHE,600398.XSHG,300422.XSHE,600291.XSHG,002462.XSHE,002388.XSHE,300137.XSHE,601106.XSHG,000777.XSHE,300394.XSHE,300567.XSHE,002862.XSHE,600876.XSHG,603416.XSHG,600460.XSHG,603388.XSHG,000005.XSHE,300112.XSHE,002379.XSHE,600732.XSHG,300505.XSHE,300659.XSHE,002541.XSHE,300458.XSHE,000702.XSHE,600004.XSHG,603360.XSHG,600602.XSHG,603011.XSHG,002405.XSHE,300637.XSHE,300188.XSHE,000909.XSHE,300381.XSHE,600123.XSHG,300502.XSHE,600250.XSHG,000697.XSHE,600221.XSHG,002719.XSHE,603728.XSHG,603879.XSHG,002328.XSHE,300138.XSHE,300276.XSHE,002213.XSHE,000809.XSHE,000045.XSHE,601369.XSHG,600166.XSHG,600800.XSHG,300440.XSHE,603658.XSHG,002807.XSHE,300216.XSHE,000719.XSHE,601500.XSHG,002774.XSHE,601628.XSHG,002696.XSHE,002550.XSHE,603617.XSHG,300169.XSHE,603286.XSHG,603869.XSHG,300419.XSHE,600223.XSHG,002879.XSHE,600622.XSHG,600288.XSHG,002268.XSHE,600305.XSHG,600189.XSHG,600674.XSHG,002755.XSHE,000063.XSHE,002440.XSHE,603559.XSHG,603598.XSHG,000919.XSHE,300617.XSHE,002637.XSHE,000048.XSHE,002702.XSHE,002677.XSHE,600965.XSHG,000586.XSHE,300604.XSHE,002629.XSHE,300318.XSHE,300402.XSHE,603330.XSHG,600853.XSHG,000883.XSHE,300282.XSHE,300470.XSHE,600652.XSHG,300623.XSHE,603033.XSHG,300359.XSHE,600482.XSHG,600226.XSHG,000997.XSHE,300184.XSHE,600493.XSHG,002181.XSHE,603639.XSHG,002748.XSHE,603086.XSHG,603200.XSHG,300068.XSHE,600343.XSHG,603315.XSHG,300113.XSHE,600785.XSHG,002049.XSHE,002350.XSHE,000877.XSHE,600746.XSHG,000756.XSHE,600889.XSHG,002467.XSHE,603616.XSHG,000856.XSHE,002139.XSHE,600917.XSHG,002201.XSHE,600346.XSHG,000975.XSHE,600240.XSHG,601225.XSHG,002845.XSHE,002818.XSHE,603225.XSHG,600835.XSHG,002641.XSHE,600843.XSHG,002224.XSHE,300625.XSHE,600675.XSHG,600397.XSHG,002546.XSHE,000713.XSHE,600326.XSHG,000158.XSHE,002873.XSHE,600161.XSHG,000800.XSHE,002736.XSHE,002406.XSHE,600337.XSHG,600372.XSHG,600729.XSHG,002028.XSHE,300627.XSHE,300235.XSHE,300221.XSHE,000539.XSHE,600776.XSHG,002380.XSHE,600503.XSHG,600227.XSHG,002372.XSHE,002222.XSHE,000430.XSHE,603603.XSHG,600319.XSHG,000690.XSHE,600416.XSHG,601965.XSHG,300214.XSHE,603189.XSHG,601008.XSHG,601933.XSHG,000861.XSHE,002187.XSHE,300240.XSHE,600761.XSHG,603918.XSHG,300498.XSHE,000965.XSHE,002067.XSHE,603335.XSHG,600665.XSHG,300315.XSHE,002018.XSHE,603058.XSHG,002113.XSHE,000620.XSHE,002564.XSHE,600626.XSHG,603101.XSHG,002466.XSHE,600499.XSHG,000159.XSHE,002498.XSHE,002500.XSHE,601858.XSHG,300247.XSHE,603721.XSHG,002223.XSHE,300510.XSHE,300320.XSHE,002285.XSHE,002853.XSHE,002470.XSHE,600113.XSHG,002123.XSHE,600751.XSHG,300329.XSHE,002563.XSHE,603813.XSHG,002009.XSHE,300557.XSHE,600367.XSHG,002003.XSHE,002134.XSHE,002441.XSHE,600477.XSHG,000502.XSHE,600526.XSHG,300119.XSHE,002605.XSHE,002813.XSHE,600132.XSHG,002266.XSHE,300203.XSHE,002362.XSHE,300529.XSHE,002216.XSHE,603223.XSHG,000415.XSHE,002384.XSHE,002209.XSHE,002370.XSHE,603985.XSHG,000722.XSHE,600425.XSHG,601766.XSHG,002126.XSHE,300123.XSHE,002286.XSHE,002726.XSHE,000701.XSHE,600330.XSHG,002805.XSHE,002290.XSHE,000949.XSHE,002419.XSHE,603000.XSHG,300518.XSHE,002412.XSHE,002185.XSHE,002729.XSHE,603698.XSHG,002865.XSHE,600643.XSHG,600540.XSHG,000732.XSHE,300429.XSHE,300488.XSHE,603797.XSHG,600220.XSHG,300571.XSHE,600576.XSHG,600577.XSHG,000977.XSHE,600748.XSHG,300355.XSHE,300512.XSHE,300008.XSHE,300560.XSHE,002478.XSHE,600438.XSHG,601798.XSHG,300605.XSHE,000717.XSHE,002491.XSHE,002451.XSHE,002524.XSHE,002135.XSHE,300147.XSHE,600583.XSHG,600531.XSHG,000931.XSHE,002229.XSHE,000903.XSHE,300245.XSHE,600020.XSHG,600459.XSHG,601231.XSHG,600476.XSHG,600710.XSHG,603839.XSHG,600323.XSHG,603843.XSHG,002095.XSHE,600887.XSHG,000716.XSHE,300476.XSHE,600783.XSHG,601898.XSHG,300183.XSHE,600696.XSHG,600269.XSHG,300642.XSHE,600671.XSHG,300700.XSHE,300187.XSHE,300408.XSHE,600649.XSHG,300482.XSHE,600467.XSHG,300255.XSHE,300120.XSHE,600999.XSHG,000514.XSHE,002250.XSHE,603703.XSHG,300236.XSHE,600874.XSHG,600505.XSHG,300264.XSHE,300225.XSHE,600317.XSHG,600623.XSHG,603636.XSHG,002480.XSHE,600255.XSHG,002056.XSHE,603578.XSHG,601567.XSHG,002144.XSHE,300533.XSHE,600030.XSHG,300479.XSHE,300205.XSHE,600855.XSHG,300319.XSHE,002884.XSHE,000488.XSHE,002890.XSHE,600743.XSHG,600695.XSHG,300122.XSHE,300446.XSHE,300480.XSHE,601949.XSHG,601616.XSHG,603038.XSHG,601618.XSHG,002543.XSHE,603500.XSHG,600823.XSHG,002106.XSHE,600616.XSHG,300608.XSHE,002817.XSHE,002773.XSHE,300364.XSHE,002054.XSHE,002575.XSHE,300049.XSHE,300686.XSHE,600235.XSHG,600977.XSHG,600241.XSHG,300577.XSHE,002578.XSHE,603113.XSHG,600570.XSHG,000036.XSHE,002349.XSHE,603730.XSHG,600481.XSHG,600426.XSHG,002038.XSHE,600355.XSHG,002514.XSHE,600869.XSHG,300081.XSHE,002770.XSHE,000779.XSHE,600677.XSHG,600369.XSHG,002310.XSHE,300328.XSHE,002398.XSHE,300094.XSHE,603776.XSHG,002232.XSHE,600555.XSHG,603005.XSHG,603609.XSHG,002714.XSHE,002163.XSHE,300078.XSHE,600794.XSHG,000590.XSHE,603599.XSHG,002042.XSHE,300161.XSHE,600690.XSHG,603444.XSHG,603368.XSHG,300665.XSHE,300172.XSHE,601258.XSHG,600307.XSHG,002611.XSHE,600153.XSHG,600598.XSHG,300501.XSHE,002080.XSHE,603387.XSHG,600079.XSHG,603997.XSHG,600569.XSHG,002072.XSHE,002444.XSHE,601126.XSHG,000601.XSHE,300070.XSHE,600758.XSHG,603001.XSHG,002027.XSHE,601058.XSHG,002566.XSHE,000587.XSHE,600211.XSHG,002705.XSHE,603027.XSHG,300127.XSHE,300012.XSHE,000729.XSHE,002477.XSHE,600137.XSHG,002108.XSHE,002572.XSHE,600600.XSHG,002761.XSHE,600233.XSHG,300248.XSHE,002488.XSHE,603077.XSHG,002439.XSHE,000789.XSHE,000801.XSHE,600735.XSHG,000726.XSHE,000411.XSHE,002838.XSHE,603602.XSHG,300129.XSHE,300160.XSHE,000830.XSHE,002394.XSHE,000959.XSHE,600232.XSHG,600768.XSHG,600537.XSHG,300576.XSHE,600340.XSHG,000710.XSHE,601901.XSHG,300442.XSHE,000917.XSHE,603955.XSHG,600586.XSHG,600150.XSHG,002875.XSHE,300062.XSHE,300130.XSHE,600201.XSHG,603669.XSHG,603586.XSHG,002391.XSHE,600395.XSHG,000709.XSHE,600738.XSHG,000595.XSHE,600848.XSHG,002668.XSHE,300336.XSHE,002681.XSHE,300696.XSHE,600567.XSHG,300520.XSHE,600699.XSHG,002321.XSHE,002287.XSHE,300067.XSHE,300468.XSHE,002395.XSHE,000525.XSHE,002878.XSHE,300447.XSHE,000990.XSHE,600256.XSHG,002200.XSHE,600766.XSHG,300592.XSHE,600814.XSHG,300028.XSHE,600585.XSHG,600396.XSHG,600178.XSHG,000963.XSHE,300514.XSHE,600658.XSHG,002590.XSHE,300126.XSHE,002790.XSHE,002648.XSHE,002850.XSHE,600329.XSHG,002599.XSHE,300237.XSHE,000568.XSHE,601398.XSHG,300500.XSHE,002751.XSHE,300676.XSHE,300053.XSHE,600073.XSHG,600523.XSHG,002309.XSHE,601929.XSHG,601700.XSHG,603505.XSHG,002511.XSHE,601928.XSHG,002011.XSHE,601601.XSHG,600111.XSHG,300011.XSHE,300460.XSHE,600410.XSHG,000897.XSHE,002407.XSHE,002561.XSHE,600651.XSHG,600435.XSHG,002513.XSHE,300569.XSHE,600782.XSHG,600352.XSHG,600122.XSHG,603528.XSHG,002461.XSHE,300194.XSHE,002759.XSHE,002742.XSHE,300441.XSHE,000419.XSHE,002484.XSHE,601377.XSHG,600703.XSHG,601390.XSHG,600845.XSHG,600727.XSHG,603665.XSHG,002150.XSHE,000916.XSHE,601368.XSHG,600615.XSHG,300165.XSHE,300176.XSHE,000547.XSHE,002165.XSHE,600496.XSHG,600998.XSHG,600775.XSHG,600612.XSHG,600805.XSHG,000882.XSHE,600668.XSHG,603258.XSHG,000890.XSHE,600841.XSHG,002588.XSHE,000989.XSHE,600120.XSHG,002197.XSHE,300690.XSHE,002152.XSHE,002366.XSHE,600031.XSHG,603069.XSHG,300079.XSHE,002809.XSHE,600359.XSHG,002274.XSHE,600285.XSHG,601211.XSHG,601857.XSHG,002275.XSHE,300074.XSHE,000721.XSHE,000020.XSHE,002455.XSHE,600716.XSHG,600297.XSHG,603798.XSHG,300199.XSHE,603566.XSHG,002724.XSHE,300521.XSHE,600292.XSHG,600316.XSHG,000815.XSHE,300602.XSHE,300230.XSHE,600128.XSHG,002005.XSHE,600229.XSHG,600490.XSHG,603168.XSHG,000498.XSHE,300080.XSHE,002348.XSHE,603036.XSHG,603458.XSHG,600590.XSHG,000034.XSHE,002767.XSHE,000551.XSHE,000605.XSHE,002355.XSHE,002653.XSHE,000409.XSHE,603268.XSHG,002167.XSHE,300334.XSHE,300125.XSHE,600380.XSHG,000885.XSHE,002202.XSHE,600536.XSHG,000665.XSHE,600765.XSHG,603527.XSHG,600075.XSHG,002718.XSHE,002735.XSHE,000518.XSHE,300535.XSHE,601015.XSHG,600362.XSHG,603859.XSHG,600265.XSHG,002791.XSHE,300585.XSHE,002219.XSHE,600090.XSHG,300232.XSHE,300558.XSHE,600121.XSHG,000793.XSHE,600630.XSHG,600653.XSHG,002207.XSHE,600097.XSHG,002086.XSHE,600448.XSHG,300611.XSHE,600808.XSHG,002673.XSHE,300455.XSHE,002283.XSHE,600873.XSHG,603778.XSHG,601000.XSHG,002313.XSHE,300298.XSHE,002138.XSHE,601016.XSHG,600138.XSHG,300534.XSHE,600967.XSHG,300044.XSHE,601375.XSHG,300523.XSHE,002779.XSHE,002193.XSHE,000985.XSHE,002852.XSHE,600858.XSHG,000937.XSHE,002393.XSHE,600321.XSHG,300106.XSHE,000548.XSHE,603881.XSHG,002208.XSHE,300157.XSHE,600399.XSHG,600449.XSHG,600691.XSHG,002112.XSHE,600210.XSHG,600469.XSHG,603828.XSHG,000626.XSHE,600571.XSHG,603637.XSHG,000410.XSHE,603569.XSHG,002231.XSHE,300185.XSHE,300146.XSHE,600483.XSHG,600054.XSHG,600834.XSHG,002280.XSHE,300220.XSHE,601168.XSHG,002555.XSHE,600547.XSHG,002111.XSHE,600406.XSHG,000978.XSHE,603633.XSHG,603123.XSHG,300229.XSHE,300409.XSHE,300616.XSHE,002655.XSHE,600861.XSHG,002069.XSHE,600376.XSHG,603060.XSHG,603079.XSHG,000566.XSHE,601333.XSHG,300191.XSHE,600067.XSHG,600741.XSHG,600519.XSHG,002612.XSHE,600521.XSHG,601117.XSHG,000829.XSHE,601222.XSHG,300378.XSHE,603726.XSHG,002597.XSHE,300685.XSHE,600217.XSHG,300396.XSHE,002267.XSHE,300432.XSHE,300213.XSHE,002895.XSHE,603885.XSHG,600103.XSHG,601388.XSHG,600298.XSHG,000589.XSHE,600351.XSHG,601339.XSHG,002014.XSHE,002613.XSHE,002326.XSHE,002342.XSHE,600556.XSHG,002753.XSHE,002687.XSHE,000070.XSHE,002822.XSHE,300341.XSHE,603165.XSHG,600192.XSHG,600444.XSHG,300610.XSHE,603041.XSHG,002889.XSHE,300406.XSHE,002545.XSHE,002238.XSHE,603508.XSHG,002633.XSHE,600237.XSHG,002234.XSHE,300032.XSHE,002711.XSHE,600582.XSHG,300099.XSHE,002483.XSHE,600510.XSHG,002752.XSHE,603222.XSHG,300029.XSHE,002343.XSHE,603889.XSHG,300257.XSHE,300159.XSHE,300636.XSHE,000018.XSHE,002334.XSHE,300296.XSHE,300002.XSHE,300326.XSHE,600495.XSHG,002255.XSHE,600795.XSHG,300204.XSHE,603696.XSHG,300337.XSHE,002243.XSHE,002196.XSHE,000609.XSHE,000893.XSHE,000565.XSHE,002149.XSHE,600390.XSHG,600231.XSHG,600919.XSHG,002824.XSHE,600037.XSHG,000858.XSHE,600436.XSHG,603886.XSHG,603129.XSHG,600185.XSHG,002271.XSHE,002737.XSHE,600689.XSHG,300312.XSHE,002240.XSHE,300486.XSHE,300682.XSHE,000042.XSHE,600109.XSHG,000582.XSHE,002237.XSHE,600997.XSHG,603519.XSHG,300107.XSHE,600318.XSHG,600158.XSHG,002062.XSHE,002041.XSHE,002464.XSHE,002340.XSHE,300057.XSHE,600191.XSHG,601137.XSHG,600071.XSHG,300449.XSHE,000610.XSHE,603906.XSHG,000835.XSHE,601186.XSHG,603819.XSHG,002552.XSHE,603488.XSHG,002279.XSHE,603515.XSHG,300578.XSHE,002022.XSHE,300483.XSHE,002661.XSHE,603978.XSHG,300238.XSHE,603898.XSHG,300306.XSHE,002316.XSHE,603888.XSHG,002081.XSHE,002608.XSHE,300681.XSHE,002833.XSHE,000703.XSHE,600987.XSHG,300054.XSHE,300004.XSHE,603158.XSHG,600206.XSHG,600660.XSHG,002241.XSHE,600693.XSHG,300239.XSHE,603305.XSHG,300618.XSHE,300382.XSHE,603333.XSHG,002492.XSHE,000655.XSHE,002164.XSHE,600538.XSHG,300023.XSHE,000969.XSHE,300450.XSHE,300348.XSHE,600839.XSHG,601101.XSHG,600159.XSHG,300591.XSHE,601595.XSHG,002826.XSHE,000593.XSHE,600584.XSHG,002044.XSHE,000738.XSHE,603035.XSHG,002065.XSHE,002698.XSHE,002421.XSHE,002585.XSHE,002471.XSHE,603331.XSHG,002636.XSHE,300289.XSHE,000792.XSHE,000795.XSHE,600779.XSHG,002032.XSHE,000973.XSHE,300061.XSHE,600050.XSHG,002177.XSHE,000667.XSHE,300545.XSHE,603031.XSHG,300108.XSHE,601677.XSHG,002045.XSHE,000001.XSHE,002159.XSHE,300181.XSHE,300323.XSHE,002332.XSHE,603678.XSHG,002685.XSHE,600115.XSHG,002433.XSHE,002645.XSHE,603630.XSHG,002783.XSHE,002203.XSHE,000012.XSHE,601872.XSHG,603768.XSHG,601908.XSHG,002273.XSHE,300110.XSHE,002587.XSHE,600900.XSHG,601997.XSHG,603518.XSHG,002709.XSHE,600170.XSHG,600797.XSHG,300392.XSHE,600247.XSHG,002886.XSHE,002117.XSHE,300683.XSHE,002615.XSHE,002446.XSHE,002401.XSHE,600026.XSHG,002299.XSHE,000952.XSHE,002194.XSHE,603023.XSHG,600055.XSHG,000023.XSHE,600642.XSHG,000757.XSHE,000818.XSHE,002743.XSHE,300038.XSHE,300445.XSHE,600157.XSHG,002800.XSHE,000039.XSHE,600939.XSHG,600116.XSHG,000980.XSHE,002745.XSHE,300219.XSHE,000597.XSHE,000408.XSHE,600167.XSHG,601163.XSHG,600180.XSHG,603313.XSHG,600207.XSHG,600893.XSHG,000796.XSHE,002035.XSHE,300552.XSHE,002560.XSHE,300517.XSHE,600361.XSHG,300009.XSHE,600507.XSHG,002496.XSHE,000685.XSHE,300473.XSHE,600152.XSHG,002716.XSHE,600976.XSHG,000807.XSHE,600763.XSHG,600363.XSHG,002317.XSHE,002402.XSHE,300102.XSHE,000418.XSHE,300331.XSHE,002603.XSHE,600970.XSHG,603338.XSHG,002214.XSHE,600282.XSHG,600038.XSHG,300638.XSHE,000686.XSHE,002493.XSHE,601318.XSHG,002827.XSHE,002457.XSHE,300196.XSHE,300358.XSHE,600311.XSHG,600489.XSHG,002319.XSHE,601611.XSHG,603383.XSHG,300294.XSHE,600151.XSHG,000680.XSHE,002792.XSHE,600393.XSHG,000672.XSHE,600816.XSHG,603716.XSHG,002236.XSHE,002127.XSHE,600881.XSHG,002424.XSHE,601518.XSHG,002084.XSHE,600546.XSHG,603933.XSHG,000981.XSHE,600613.XSHG,000767.XSHE,000523.XSHE,601966.XSHG,002689.XSHE,601939.XSHG,601555.XSHG,300386.XSHE,002810.XSHE,000892.XSHE,002750.XSHE,600880.XSHG,002692.XSHE,002747.XSHE,601900.XSHG,601992.XSHG,300371.XSHE,600057.XSHG,002772.XSHE,002358.XSHE,300198.XSHE,600654.XSHG,600418.XSHG,002107.XSHE,600478.XSHG,300643.XSHE,603198.XSHG,002565.XSHE,000727.XSHE,002251.XSHE,601226.XSHG,000513.XSHE,002642.XSHE,002148.XSHE,603986.XSHG,002427.XSHE,300511.XSHE,601801.XSHG,002428.XSHE,603656.XSHG,000066.XSHE,600035.XSHG,000961.XSHE,603320.XSHG,300024.XSHE,300206.XSHE,603111.XSHG,603277.XSHG,603369.XSHG,600767.XSHG,002300.XSHE,002832.XSHE,300271.XSHE,002182.XSHE,600683.XSHG,600312.XSHG,603689.XSHG,002540.XSHE,002269.XSHE,300655.XSHE,600082.XSHG,300252.XSHE,603959.XSHG,002404.XSHE,000040.XSHE,002276.XSHE,000826.XSHE,000902.XSHE,600565.XSHG,600400.XSHG,300046.XSHE,603429.XSHG,002882.XSHE,600112.XSHG,300316.XSHE,002548.XSHE,603398.XSHG,300144.XSHE,603787.XSHG,002308.XSHE,002217.XSHE,300246.XSHE,300566.XSHE,603098.XSHG,600730.XSHG,300016.XSHE,603309.XSHG,600558.XSHG,600094.XSHG,603010.XSHG,002786.XSHE,601800.XSHG,601003.XSHG,000557.XSHE,600335.XSHG,300485.XSHE,601208.XSHG,000151.XSHE,002778.XSHE,300424.XSHE,600197.XSHG,600838.XSHG,603668.XSHG,000413.XSHE,002515.XSHE,600745.XSHG,600737.XSHG,300170.XSHE,000908.XSHE,002311.XSHE,300369.XSHE,002558.XSHE,600309.XSHG,002738.XSHE,300390.XSHE,002620.XSHE,603980.XSHG,002544.XSHE,002430.XSHE,002188.XSHE,000537.XSHE,601880.XSHG,002074.XSHE,000993.XSHE,002679.XSHE,603116.XSHG,002190.XSHE,002344.XSHE,300273.XSHE,603556.XSHG,600509.XSHG,600306.XSHG,300428.XSHE,300370.XSHE,603298.XSHG,002248.XSHE,600354.XSHG,601010.XSHG,300506.XSHE,600770.XSHG,300548.XSHE,300075.XSHE,603167.XSHG,600637.XSHG,002025.XSHE,300037.XSHE,002609.XSHE,002387.XSHE,002385.XSHE,600879.XSHG,300014.XSHE,600895.XSHG,600379.XSHG,002628.XSHE,002438.XSHE,000921.XSHE,000501.XSHE,002843.XSHE,600061.XSHG,600680.XSHG,603180.XSHG,300606.XSHE,002847.XSHE,000825.XSHE,000652.XSHE,002047.XSHE,300662.XSHE,000971.XSHE,002277.XSHE,002226.XSHE,600756.XSHG,002007.XSHE,603688.XSHG,600290.XSHG,600303.XSHG,300030.XSHE,002019.XSHE,600033.XSHG,300065.XSHE,300069.XSHE,000859.XSHE,300474.XSHE,002610.XSHE,300403.XSHE,600117.XSHG,600313.XSHG,603456.XSHG,300304.XSHE,002151.XSHE,000839.XSHE,002376.XSHE,002749.XSHE,300656.XSHE,002825.XSHE,002077.XSHE,600872.XSHG,600996.XSHG,600993.XSHG,300438.XSHE,603042.XSHG,603138.XSHG,601886.XSHG,000813.XSHE,300321.XSHE,600661.XSHG,002221.XSHE,000333.XSHE,001979.XSHE,601188.XSHG,002304.XSHE,601021.XSHG,600212.XSHG,603966.XSHG,002651.XSHE,002184.XSHE,000958.XSHE,300283.XSHE,000060.XSHE,600104.XSHG,300133.XSHE,002508.XSHE,600697.XSHG,603345.XSHG,002580.XSHE,002649.XSHE,002120.XSHE,603969.XSHG,603589.XSHG,000731.XSHE,300526.XSHE,300436.XSHE,002746.XSHE,300076.XSHE,600051.XSHG,000402.XSHE,002158.XSHE,600203.XSHG,002519.XSHE,600886.XSHG,601969.XSHG,002227.XSHE,002052.XSHE,002860.XSHE,300209.XSHE,300314.XSHE,600759.XSHG,601229.XSHG,603536.XSHG,002386.XSHE,300346.XSHE,600644.XSHG,300284.XSHE,000425.XSHE,603318.XSHG,002270.XSHE,601919.XSHG,300542.XSHE,603757.XSHG,300393.XSHE,300327.XSHE,000737.XSHE,600866.XSHG,600289.XSHG,601020.XSHG,000584.XSHE,600105.XSHG,002811.XSHE,002204.XSHE,300515.XSHE,600936.XSHG,002863.XSHE,002690.XSHE,603016.XSHG,002212.XSHE,601669.XSHG,002425.XSHE,300651.XSHE,601588.XSHG,002162.XSHE,002400.XSHE,600984.XSHG,000695.XSHE,603900.XSHG,002501.XSHE,000831.XSHE,600595.XSHG,600609.XSHG,600545.XSHG,002533.XSHE,300582.XSHE,601566.XSHG,600187.XSHG,002707.XSHE,601212.XSHG,002614.XSHE,300596.XSHE,002115.XSHE,603628.XSHG,300531.XSHE,300189.XSHE,300509.XSHE,300243.XSHE,002712.XSHE,000718.XSHE,603063.XSHG,002381.XSHE,600533.XSHG,002195.XSHE,300202.XSHE,002114.XSHE,603611.XSHG,600796.XSHG,600829.XSHG,600836.XSHG,002869.XSHE,000962.XSHE,603385.XSHG,000545.XSHE,600284.XSHG,600764.XSHG,300701.XSHE,300116.XSHE,601216.XSHG,000561.XSHE,300435.XSHE,002253.XSHE,002654.XSHE,300469.XSHE,600773.XSHG,000421.XSHE,300043.XSHE,600884.XSHG,601127.XSHG,002765.XSHE,001896.XSHE,600573.XSHG,002339.XSHE,300491.XSHE,603717.XSHG,002104.XSHE,002064.XSHE,002374.XSHE,600345.XSHG,002140.XSHE,600133.XSHG,603269.XSHG,600078.XSHG,002502.XSHE,000009.XSHE,000982.XSHE,603990.XSHG,000776.XSHE,601100.XSHG,000983.XSHE,601789.XSHG,603612.XSHG,000918.XSHE,002456.XSHE,300330.XSHE,603017.XSHG,601881.XSHG,600486.XSHG,603991.XSHG,603989.XSHG,603067.XSHG,300597.XSHE,002046.XSHE,002490.XSHE,002090.XSHE,002118.XSHE,300675.XSHE,600268.XSHG,601228.XSHG,000957.XSHE,002327.XSHE,002730.XSHE,000819.XSHE,600419.XSHG,600498.XSHG,300387.XSHE,000608.XSHE,603357.XSHG,002839.XSHE,601866.XSHG,300332.XSHE,600714.XSHG,600587.XSHG,002294.XSHE,300031.XSHE,000678.XSHE,600684.XSHG,300305.XSHE,300027.XSHE,002071.XSHE,002292.XSHE,002551.XSHE,000677.XSHE,300399.XSHE,000037.XSHE,600641.XSHG,300540.XSHE,300105.XSHE,601116.XSHG,002768.XSHE,000911.XSHE,600828.XSHG,002639.XSHE,300433.XSHE,300352.XSHE,600599.XSHG,002017.XSHE,603020.XSHG,002618.XSHE,300088.XSHE,000998.XSHE,600798.XSHG,002435.XSHE,300293.XSHE,002235.XSHE,002454.XSHE,603868.XSHG,600462.XSHG,603386.XSHG,002215.XSHE,600405.XSHG,002713.XSHE,002105.XSHE,603043.XSHG,002549.XSHE,600048.XSHG,300036.XSHE,603789.XSHG,002390.XSHE,600909.XSHG,600784.XSHG,002532.XSHE,000599.XSHE,300463.XSHE,601199.XSHG,300353.XSHE,601918.XSHG,600596.XSHG,002338.XSHE,600009.XSHG,002571.XSHE,002507.XSHE,600360.XSHG,600348.XSHG,000888.XSHE,002891.XSHE,603393.XSHG,002085.XSHE,600218.XSHG,600257.XSHG,002186.XSHE,000526.XSHE,603359.XSHG,300452.XSHE,300613.XSHE,600135.XSHG,601727.XSHG,600981.XSHG,600811.XSHG,002040.XSHE,600966.XSHG,600099.XSHG,300609.XSHE,300066.XSHE,000922.XSHE,002136.XSHE,600018.XSHG,002230.XSHE,603026.XSHG,300619.XSHE,002861.XSHE,300091.XSHE,002660.XSHE,002801.XSHE,300669.XSHE,000761.XSHE,601818.XSHG,000881.XSHE,002218.XSHE,000622.XSHE,600333.XSHG,002667.XSHE,600388.XSHG,600678.XSHG,600439.XSHG,300493.XSHE,600961.XSHG,002592.XSHE,600572.XSHG,300005.XSHE,300072.XSHE,000671.XSHE,603767.XSHG,000032.XSHE,300430.XSHE,600382.XSHG,002688.XSHE,000536.XSHE,300639.XSHE,002760.XSHE,300383.XSHE,002495.XSHE,300101.XSHE,600867.XSHG,300193.XSHE,002727.XSHE,603326.XSHG,300357.XSHE,002820.XSHE,600755.XSHG,002527.XSHE,002574.XSHE,002489.XSHE,600614.XSHG,000939.XSHE,000899.XSHE,300003.XSHE,603801.XSHG,000530.XSHE,002037.XSHE,000683.XSHE,600705.XSHG,002119.XSHE,002073.XSHE,600592.XSHG,600588.XSHG,300351.XSHE,002849.XSHE,002703.XSHE,601177.XSHG,002803.XSHE,600549.XSHG,002870.XSHE,002013.XSHE,002448.XSHE,603085.XSHG,002503.XSHE,300026.XSHE,002183.XSHE,600208.XSHG,600971.XSHG,002758.XSHE,002422.XSHE,002145.XSHE,300575.XSHE,300154.XSHE,600415.XSHG,000778.XSHE,600704.XSHG,600726.XSHG,000828.XSHE,600251.XSHG,000521.XSHE,000014.XSHE,000625.XSHE,601699.XSHG,002093.XSHE,600072.XSHG,300629.XSHE,300297.XSHE,002868.XSHE,300519.XSHE,600815.XSHG,300259.XSHE,601958.XSHG,000571.XSHE,000976.XSHE,002732.XSHE,600491.XSHG,002192.XSHE,000338.XSHE,002521.XSHE,300663.XSHE,603227.XSHG,300595.XSHE,002157.XSHE,300285.XSHE,300117.XSHE,002346.XSHE,002686.XSHE,000069.XSHE,002172.XSHE,603626.XSHG,300317.XSHE,600093.XSHG,600198.XSHG,002242.XSHE,002472.XSHE,600908.XSHG,600963.XSHG,300017.XSHE,000581.XSHE,000153.XSHE,002700.XSHE,300380.XSHE,300158.XSHE,002368.XSHE,002420.XSHE,603638.XSHG,300391.XSHE,600168.XSHG,300047.XSHE,002244.XSHE,002584.XSHE,002220.XSHE,000088.XSHE,300660.XSHE,000750.XSHE,600098.XSHG,300667.XSHE,002640.XSHE,600086.XSHG,002103.XSHE,002061.XSHE,000635.XSHE,600747.XSHG,300299.XSHE,300697.XSHE,002570.XSHE,002762.XSHE,300645.XSHE,600875.XSHG,000028.XSHE,600568.XSHG,600781.XSHG,000708.XSHE,002866.XSHE,601009.XSHG,603007.XSHG,603066.XSHG,600856.XSHG,603882.XSHG,002154.XSHE,600193.XSHG,600463.XSHG,002010.XSHE,002125.XSHE,002246.XSHE,600734.XSHG,601011.XSHG,600865.XSHG,603355.XSHG,000999.XSHE,603078.XSHG,002616.XSHE,600629.XSHG,600260.XSHG,300640.XSHE,002663.XSHE,600820.XSHG,002147.XSHE,002728.XSHE,601128.XSHG,002591.XSHE,603567.XSHG,601515.XSHG,000929.XSHE,603595.XSHG,000541.XSHE,601608.XSHG,300042.XSHE,300584.XSHE,603608.XSHG,300278.XSHE,300379.XSHE,600202.XSHG,002434.XSHE,002211.XSHE,600502.XSHG,300499.XSHE,000960.XSHE,002819.XSHE,600760.XSHG,002437.XSHE,300513.XSHE,603738.XSHG,603181.XSHG,002101.XSHE,002325.XSHE,600213.XSHG,000056.XSHE,300532.XSHE,603126.XSHG,300457.XSHE,000966.XSHE,600983.XSHG,002535.XSHE,603825.XSHG,300425.XSHE,603866.XSHG,300628.XSHE,300217.XSHE,601336.XSHG,300261.XSHE,600186.XSHG,002528.XSHE,600657.XSHG,002896.XSHE,300536.XSHE,002417.XSHE,600980.XSHG,603233.XSHG,000416.XSHE,300401.XSHE,002023.XSHE,002657.XSHE,300268.XSHE,600833.XSHG,000712.XSHE,000851.XSHE,002146.XSHE,600844.XSHG,600753.XSHG,300231.XSHE,002662.XSHE,002851.XSHE,002626.XSHE,600008.XSHG,603127.XSHG,603901.XSHG,600862.XSHG,603517.XSHG,002322.XSHE,603727.XSHG,002485.XSHE,300385.XSHE,002142.XSHE,000423.XSHE,000786.XSHE,000905.XSHE,002812.XSHE,000833.XSHE,000705.XSHE,300365.XSHE,002664.XSHE,000698.XSHE,603308.XSHG,600266.XSHG,600679.XSHG,300195.XSHE,601985.XSHG,603880.XSHG,002131.XSHE,600230.XSHG,603737.XSHG,002329.XSHE,000407.XSHE,600058.XSHG,603615.XSHG,600721.XSHG,002516.XSHE,002721.XSHE,002284.XSHE,000848.XSHE,002796.XSHE,600634.XSHG,300128.XSHE,002594.XSHE,000058.XSHE,600897.XSHG,300098.XSHE,300211.XSHE,300141.XSHE,000735.XSHE,002600.XSHE,600069.XSHG,603929.XSHG,603779.XSHG,002121.XSHE,002297.XSHE,600802.XSHG,300693.XSHE,601233.XSHG,600162.XSHG,600497.XSHG,000429.XSHE,600962.XSHG,002463.XSHE,603208.XSHG,002002.XSHE,000762.XSHE,002855.XSHE,600560.XSHG,300301.XSHE,300350.XSHE,600275.XSHG,000669.XSHE,000417.XSHE,601001.XSHG,000573.XSHE,300478.XSHE,002632.XSHE,002476.XSHE,000558.XSHE,600019.XSHG,300052.XSHE,300633.XSHE,600287.XSHG,300666.XSHE,600518.XSHG,002734.XSHE,600750.XSHG,002375.XSHE,002468.XSHE,300395.XSHE,002063.XSHE,601139.XSHG,000691.XSHE,603690.XSHG,300626.XSHE,300018.XSHE,600562.XSHG,601328.XSHG,300680.XSHE,600455.XSHG,002096.XSHE,300139.XSHE,002892.XSHE,300546.XSHE,002191.XSHE,603421.XSHG,300151.XSHE,603358.XSHG,000639.XSHE,000933.XSHE,000880.XSHE,300166.XSHE,002815.XSHE,000739.XSHE,601088.XSHG,002583.XSHE,600821.XSHG,603021.XSHG,002793.XSHE,603557.XSHG,600650.XSHG,601882.XSHG,600063.XSHG,002816.XSHE,002695.XSHE,300007.XSHE,002445.XSHE,000759.XSHE,601099.XSHG,002666.XSHE,603025.XSHG,600283.XSHG,300025.XSHE,300543.XSHE,600125.XSHG,000799.XSHE,000591.XSHE,000837.XSHE,603019.XSHG,600723.XSHG,002088.XSHE,002408.XSHE,600403.XSHG,002771.XSHE,000788.XSHE,603808.XSHG,300632.XSHE,002582.XSHE,600101.XSHG,300551.XSHE,603177.XSHG,002579.XSHE,603555.XSHG,002160.XSHE,600990.XSHG,300374.XSHE,601599.XSHG,600293.XSHG,600633.XSHG,603288.XSHG,300599.XSHE,603228.XSHG,300653.XSHE,002777.XSHE,603818.XSHG,600017.XSHG,002797.XSHE,002769.XSHE,300668.XSHE,300168.XSHE,000687.XSHE,002474.XSHE,300453.XSHE,600386.XSHG,000938.XSHE,601107.XSHG,000673.XSHE,603968.XSHG,002016.XSHE,300167.XSHE,300035.XSHE,600243.XSHG,002124.XSHE,600868.XSHG,600310.XSHG,002547.XSHE,600508.XSHG,000886.XSHE,600028.XSHG,600060.XSHG,603987.XSHG,603496.XSHG,002353.XSHE,002258.XSHE,600552.XSHG,603088.XSHG,300481.XSHE,600557.XSHG,600515.XSHG,600011.XSHG,000860.XSHE,600215.XSHG,002087.XSHE,000915.XSHE,603139.XSHG,603203.XSHG,603579.XSHG,603766.XSHG,600234.XSHG,600007.XSHG,600792.XSHG,603183.XSHG,000516.XSHE,600452.XSHG,603089.XSHG,300397.XSHE,000004.XSHE,002079.XSHE,300539.XSHE,300565.XSHE,600039.XSHG,600898.XSHG,002099.XSHE,300579.XSHE,603606.XSHG,300556.XSHE,300375.XSHE,600645.XSHG,600391.XSHG,603686.XSHG,300615.XSHE,002494.XSHE,600320.XSHG,603096.XSHG,300497.XSHE,300224.XSHE,600580.XSHG,600636.XSHG,000637.XSHE,002848.XSHE,000797.XSHE,600365.XSHG,600739.XSHG,300559.XSHE,300550.XSHE,002522.XSHE,002265.XSHE,300554.XSHE,600847.XSHG,300541.XSHE,603699.XSHG,300338.XSHE,000700.XSHE,000650.XSHE,300342.XSHE,603266.XSHG,002568.XSHE,300266.XSHE,600252.XSHG,000022.XSHE,600757.XSHG,002094.XSHE,300250.XSHE,000753.XSHE,601688.XSHG,002228.XSHE,600083.XSHG,002562.XSHE,002876.XSHE,300538.XSHE,603199.XSHG,600992.XSHG,600539.XSHG,600708.XSHG,300208.XSHE,000811.XSHE,300388.XSHE,000768.XSHE,600686.XSHG,300201.XSHE,600851.XSHG,002517.XSHE,002288.XSHE,600744.XSHG,300210.XSHE,600148.XSHG,600610.XSHG,603018.XSHG,600860.XSHG,600817.XSHG,002354.XSHE,600429.XSHG,601988.XSHG,000528.XSHE,002479.XSHE,600790.XSHG,603188.XSHG,300437.XSHE,600149.XSHG,002776.XSHE,300256.XSHE,002128.XSHE,000600.XSHE,600608.XSHG,601166.XSHG,300673.XSHE,300311.XSHE,000560.XSHE,601888.XSHG,300041.XSHE,002644.XSHE,002278.XSHE,600301.XSHG,002170.XSHE,002155.XSHE,300487.XSHE,300621.XSHE,300367.XSHE,601558.XSHG,002051.XSHE,300568.XSHE,600322.XSHG,600143.XSHG,603799.XSHG,300020.XSHE,300095.XSHE,600216.XSHG,300260.XSHE,600597.XSHG,002877.XSHE,600635.XSHG,002529.XSHE,002893.XSHE,300363.XSHE,000715.XSHE,603663.XSHG,002122.XSHE,300021.XSHE,603926.XSHG,002697.XSHE,000758.XSHE,603667.XSHG,600605.XSHG,600692.XSHG,600299.XSHG,600662.XSHG,002282.XSHE,300039.XSHE,600332.XSHG,300622.XSHE,300142.XSHE,600278.XSHG,603232.XSHG,300407.XSHE,002414.XSHE,000059.XSHE,000628.XSHE,000505.XSHE,002593.XSHE,600712.XSHG,600422.XSHG,002499.XSHE,300015.XSHE,002307.XSHE,000559.XSHE,300281.XSHE,300495.XSHE,300516.XSHE,002210.XSHE,300215.XSHE,002206.XSHE,002174.XSHE,002799.XSHE,600787.XSHG,002674.XSHE,600749.XSHG,002699.XSHE,600824.XSHG,000065.XSHE,002881.XSHE,600882.XSHG,300322.XSHE,000630.XSHE,603979.XSHG,600827.XSHG,600706.XSHG,000636.XSHE,002510.XSHE,600594.XSHG,603337.XSHG,603800.XSHG,002198.XSHE,000725.XSHE,600327.XSHG,000996.XSHE,002830.XSHE,002249.XSHE,603823.XSHG,000863.XSHE,300699.XSHE,300013.XSHE,002795.XSHE,000553.XSHE,600200.XSHG,000552.XSHE,600780.XSHG,002883.XSHE,002109.XSHE,600728.XSHG,600421.XSHG,600724.XSHG,603601.XSHG,300631.XSHE,300507.XSHE,002808.XSHE,300084.XSHE,300277.XSHE,600276.XSHG,600338.XSHG,002089.XSHE,000923.XSHE,002301.XSHE,603648.XSHG,002397.XSHE,300173.XSHE,002330.XSHE,601996.XSHG,300345.XSHE,600969.XSHG,002324.XSHE,300274.XSHE,603919.XSHG,000510.XSHE,000010.XSHE,002323.XSHE,002706.XSHE,002161.XSHE,600258.XSHG,300448.XSHE,603229.XSHG,300313.XSHE,603679.XSHG,002829.XSHE,002303.XSHE,600375.XSHG,603030.XSHG,603928.XSHG,300496.XSHE,300377.XSHE,600006.XSHG,603855.XSHG,300270.XSHE,000810.XSHE,002429.XSHE,600423.XSHG,601799.XSHG,600222.XSHG,600281.XSHG,600461.XSHG,300691.XSHE,603160.XSHG,002378.XSHE,002672.XSHE,000798.XSHE,603806.XSHG,000692.XSHE,300484.XSHE,600480.XSHG,300175.XSHE,002352.XSHE,000428.XSHE,600409.XSHG,300218.XSHE,002179.XSHE,000016.XSHE,601998.XSHG,600280.XSHG,002078.XSHE,600819.XSHG,603939.XSHG,300162.XSHE,600688.XSHG,300593.XSHE,002512.XSHE,002377.XSHE,600273.XSHG,603988.XSHG,300083.XSHE,002691.XSHE,000987.XSHE,002315.XSHE,603321.XSHG,601002.XSHG,300356.XSHE,300124.XSHE,601636.XSHG,000531.XSHE,300001.XSHE,300253.XSHE,000157.XSHE,002302.XSHE,600129.XSHG,600373.XSHG,603660.XSHG,002367.XSHE,000823.XSHE,600131.XSHG,603032.XSHG,000632.XSHE,002627.XSHE,600619.XSHG,300118.XSHE,600742.XSHG,600664.XSHG,002036.XSHE,000898.XSHE,603538.XSHG,601326.XSHG,300412.XSHE,300426.XSHE,600731.XSHG,603996.XSHG,300251.XSHE,002066.XSHE,603012.XSHG,002460.XSHE,600261.XSHG,002293.XSHE,603883.XSHG,600846.XSHG,300171.XSHE,600988.XSHG,600522.XSHG,300658.XSHE,600016.XSHG,000711.XSHE,300200.XSHE,300695.XSHE,600551.XSHG,600271.XSHG,002888.XSHE,603322.XSHG,002060.XSHE,600350.XSHG,002598.XSHE,600529.XSHG,002898.XSHE,600470.XSHG,000930.XSHE,000078.XSHE,300601.XSHE,002554.XSHE,600543.XSHG,300421.XSHE,300411.XSHE,300132.XSHE,601198.XSHG,600184.XSHG,002180.XSHE,603303.XSHG,000900.XSHE,600385.XSHG,300179.XSHE,300135.XSHE,600171.XSHG,300389.XSHE,002831.XSHE,600056.XSHG,603535.XSHG,600702.XSHG,300339.XSHE,002656.XSHE,002780.XSHE,002788.XSHE,000150.XSHE,600315.XSHG,603896.XSHG,300537.XSHE,603166.XSHG,600177.XSHG,600621.XSHG,300549.XSHE,600663.XSHG,002775.XSHE,002537.XSHE,002785.XSHE,300180.XSHE,600089.XSHG,002643.XSHE,002133.XSHE,300420.XSHE,002680.XSHE,600012.XSHG,300333.XSHE,000631.XSHE,603858.XSHG,300226.XSHE,600647.XSHG,300150.XSHE,000546.XSHE,002008.XSHE,000906.XSHE,002033.XSHE,601619.XSHG,300131.XSHE,300652.XSHE,002581.XSHE,603580.XSHG,600488.XSHG,300362.XSHE,600511.XSHG,603920.XSHG,300573.XSHE,300456.XSHE,000603.XSHE,603022.XSHG,002254.XSHE,000520.XSHE,002899.XSHE,600501.XSHG,600578.XSHG,002055.XSHE,600308.XSHG,603816.XSHG,002178.XSHE,600126.XSHG,000049.XSHE,002841.XSHE,000507.XSHE,000936.XSHE,300677.XSHE,600246.XSHG,002458.XSHE,600532.XSHG,000682.XSHE,002132.XSHE,000951.XSHE,603908.XSHG,600172.XSHG,603100.XSHG,603339.XSHG,300324.XSHE,000912.XSHE,300572.XSHE,600525.XSHG,600219.XSHG,002539.XSHE,000030.XSHE,000816.XSHE,002030.XSHE,600892.XSHG,002336.XSHE,603159.XSHG,000752.XSHE,002314.XSHE,603708.XSHG,000025.XSHE,000623.XSHE,300254.XSHE,600978.XSHG,000567.XSHE,300471.XSHE,600926.XSHG,600685.XSHG,000822.XSHE,600528.XSHG,000707.XSHE,002624.XSHE,002102.XSHE,300503.XSHE,000533.XSHE,002392.XSHE,600052.XSHG,002798.XSHE,000021.XSHE,600603.XSHG,000089.XSHE,603826.XSHG,000616.XSHE,000657.XSHE,601668.XSHG,002004.XSHE,603366.XSHG,300300.XSHE,300344.XSHE,002840.XSHE,600107.XSHG,600831.XSHG,002542.XSHE,002225.XSHE,600801.XSHG,600487.XSHG,603178.XSHG,002083.XSHE,300661.XSHE,600618.XSHG,603558.XSHG,600175.XSHG,002553.XSHE,300581.XSHE,300335.XSHE,000400.XSHE,002432.XSHE,600973.XSHG,603008.XSHG,600979.XSHG,601991.XSHG,002887.XSHE,600236.XSHG,300679.XSHE,002205.XSHE,300648.XSHE,000668.XSHE,603218.XSHG,300286.XSHE,300630.XSHE,002693.XSHE,600119.XSHG,002403.XSHE,600085.XSHG,002482.XSHE,002026.XSHE,002871.XSHE,000517.XSHE,600611.XSHG,300155.XSHE,600818.XSHG,000876.XSHE,000062.XSHE,300190.XSHE,002116.XSHE,600456.XSHG,300152.XSHE,300056.XSHE,603319.XSHG,002318.XSHE,600195.XSHG,300093.XSHE,002589.XSHE,600068.XSHG,603999.XSHG,002631.XSHE,603037.XSHG,600165.XSHG,002296.XSHE,000011.XSHE,002475.XSHE,603306.XSHG,300242.XSHE,600188.XSHG,300405.XSHE,603568.XSHG,002538.XSHE,603520.XSHG,600173.XSHG,000852.XSHE,300087.XSHE,600639.XSHG,300525.XSHE,300687.XSHE,300360.XSHE,300451.XSHE,603050.XSHG,300561.XSHE,002567.XSHE,000026.XSHE,600885.XSHG,300349.XSHE,601218.XSHG,000670.XSHE,300325.XSHE,002708.XSHE,300417.XSHE,600864.XSHG,000046.XSHE,002842.XSHE,600740.XSHG,002602.XSHE,000968.XSHE,600377.XSHG,603707.XSHG,600325.XSHG,600593.XSHG,601777.XSHG,002782.XSHE,002885.XSHE,002291.XSHE,002423.XSHE,603108.XSHG,300073.XSHE,000955.XSHE,300103.XSHE,300555.XSHE,000901.XSHE,002233.XSHE,601311.XSHG,600141.XSHG,601288.XSHG,603600.XSHG,002857.XSHE,601111.XSHG,600238.XSHG,603196.XSHG,603822.XSHG,002261.XSHE,002100.XSHE,601069.XSHG,300494.XSHE,002039.XSHE,600711.XSHG,000156.XSHE,002359.XSHE,000869.XSHE,600566.XSHG,601877.XSHG,000932.XSHE,000972.XSHE,300465.XSHE,300136.XSHE,002436.XSHE,600366.XSHG,601118.XSHG,000676.XSHE,603618.XSHG,603389.XSHG,002383.XSHE,600479.XSHG,000519.XSHE,300275.XSHE,002536.XSHE,600446.XSHG,300086.XSHE,000925.XSHE,601899.XSHG,300698.XSHE,002665.XSHE,600620.XSHG,002048.XSHE,601878.XSHG,600381.XSHG,600295.XSHG,600088.XSHG,000055.XSHE,600022.XSHG,300153.XSHE,300530.XSHE,000002.XSHE,002043.XSHE,000619.XSHE,002520.XSHE,000627.XSHE,300228.XSHE,600960.XSHG,600062.XSHG,603238.XSHG,300607.XSHE,002057.XSHE,600687.XSHG,000728.XSHE,600810.XSHG,601678.XSHG,601808.XSHG,603117.XSHG,300269.XSHE,300048.XSHE,300586.XSHE,600777.XSHG,002272.XSHE,300033.XSHE,600064.XSHG,000895.XSHE,002678.XSHE,603028.XSHG,601179.XSHG,300249.XSHE,300292.XSHE,300459.XSHE,600458.XSHG,603133.XSHG,300010.XSHE,002173.XSHE,002617.XSHE,300508.XSHE,002410.XSHE,603323.XSHG,600863.XSHG,002766.XSHE,300207.XSHE,603878.XSHG,600854.XSHG,000733.XSHE,603577.XSHG,002396.XSHE,002091.XSHE,300522.XSHE,600894.XSHG,300310.XSHE,600383.XSHG,300182.XSHE,300547.XSHE,600826.XSHG,300598.XSHE,600096.XSHG,002846.XSHE,300303.XSHE,300223.XSHE,002604.XSHE,002701.XSHE,300233.XSHE,002559.XSHE,600812.XSHG,000617.XSHE,600300.XSHG,300077.XSHE,002199.XSHE,600076.XSHG,300527.XSHE,002068.XSHE,601028.XSHG,000790.XSHE,603877.XSHG,300467.XSHE,600015.XSHG,000785.XSHE,600070.XSHG,000570.XSHE,601952.XSHG,002465.XSHE,002443.XSHE,000538.XSHE,002836.XSHE,603316.XSHG,300174.XSHE,002239.XSHE,600850.XSHG,600199.XSHG,600517.XSHG,603311.XSHG,600000.XSHG,600183.XSHG,600771.XSHG,601666.XSHG,300650.XSHE,600859.XSHG,600475.XSHG,000913.XSHE,600791.XSHG,002351.XSHE,000679.XSHE,002020.XSHE,000007.XSHE,600527.XSHG,002176.XSHE,603002.XSHG,300006.XSHE,300354.XSHE,000532.XSHE,002731.XSHE,002333.XSHE,000661.XSHE,300287.XSHE,600589.XSHG,600958.XSHG,600754.XSHG,600500.XSHG,603128.XSHG,603099.XSHG,600196.XSHG,601007.XSHG,000988.XSHE,002335.XSHE,000563.XSHE,002298.XSHE,603811.XSHG,600156.XSHG,603239.XSHG,002897.XSHE,600080.XSHG,000598.XSHE,002647.XSHE,002034.XSHE,603336.XSHG,000926.XSHE,603186.XSHG,600259.XSHG,600190.XSHG,600713.XSHG,603833.XSHG,000666.XSHE,002345.XSHE,000791.XSHE,002505.XSHE,601366.XSHG,002059.XSHE,600667.XSHG,300443.XSHE,300263.XSHE,300670.XSHE,002481.XSHE,300528.XSHE,603860.XSHG,300071.XSHE,603777.XSHG,600535.XSHG,000404.XSHE,601038.XSHG,600077.XSHG,002835.XSHE,002675.XSHE,300244.XSHE,002050.XSHE,600516.XSHG,300423.XSHE,000920.XSHE,000613.XSHE,002534.XSHE,000096.XSHE,002577.XSHE,603380.XSHG,000426.XSHE,600176.XSHG,000166.XSHE,002360.XSHE,000760.XSHE,002858.XSHE,603998.XSHG,000544.XSHE,603718.XSHG,603676.XSHG'
    all_code = all_code.split(',')
    count = 0
    for code in all_code:
        print(code)
        print(count)
        cal_return(code, DAYS)
        count += 1
