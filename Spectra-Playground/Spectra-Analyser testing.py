# Spectra-Analyser testing

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import scipy.signal as sig


plt.style.use("seaborn-v0_8-whitegrid")

# X-axis (energy) is spectra bins* ev/channel
energies = np.array([0.5,20.5,40.5,60.5,80.4,100.4,120.4,140.4,160.4,180.4,200.4,220.3,240.3,260.3,280.3,300.3,320.3,340.3,360.2,380.2,400.2,420.2,440.2,460.2,480.2,500.1,520.1,540.1,560.1,580.1,600.1,620.1,640,660,680,700,720,740,760,779.9,799.9,819.9,839.9,859.9,879.9,899.9,919.8,939.8,959.8,979.8,999.8,1019.8,1039.8,1059.8,1079.7,1099.7,1119.7,1139.7,1159.7,1179.7,1199.7,1219.6,1239.6,1259.6,1279.6,1299.6,1319.6,1339.6,1359.5,1379.5,1399.5,1419.5,1439.5,1459.5,1479.5,1499.4,1519.4,1539.4,1559.4,1579.4,1599.4,1619.4,1639.3,1659.3,1679.3,1699.3,1719.3,1739.3,1759.3,1779.2,1799.2,1819.2,1839.2,1859.2,1879.2,1899.2,1919.1,1939.1,1959.1,1979.1,1999.1,2019.1,2039.1,2059,2079,2099,2119,2139,2159,2179,2199,2218.9,2238.9,2258.9,2278.9,2298.9,2318.9,2338.9,2358.8,2378.8,2398.8,2418.8,2438.8,2458.8,2478.8,2498.7,2518.7,2538.7,2558.7,2578.7,2598.7,2618.7,2638.6,2658.6,2678.6,2698.6,2718.6,2738.6,2758.6,2778.5,2798.5,2818.5,2838.5,2858.5,2878.5,2898.5,2918.4,2938.4,2958.4,2978.4,2998.4,3018.4,3038.4,3058.3,3078.3,3098.3,3118.3,3138.3,3158.3,3178.3,3198.3,3218.2,3238.2,3258.2,3278.2,3298.2,3318.2,3338.2,3358.1,3378.1,3398.1,3418.1,3438.1,3458.1,3478.1,3498,3518,3538,3558,3578,3598,3618,3637.9,3657.9,3677.9,3697.9,3717.9,3737.9,3757.9,3777.8,3797.8,3817.8,3837.8,3857.8,3877.8,3897.8,3917.7,3937.7,3957.7,3977.7,3997.7,4017.7,4037.7,4057.6,4077.6,4097.6,4117.6,4137.6,4157.6,4177.6,4197.5,4217.5,4237.5,4257.5,4277.5,4297.5,4317.5,4337.5,4357.4,4377.4,4397.4,4417.4,4437.4,4457.4,4477.4,4497.3,4517.3,4537.3,4557.3,4577.3,4597.3,4617.3,4637.2,4657.2,4677.2,4697.2,4717.2,4737.2,4757.2,4777.1,4797.1,4817.1,4837.1,4857.1,4877.1,4897.1,4917,4937,4957,4977,4997,5017,5037,5056.9,5076.9,5096.9,5116.9,5136.9,5156.9,5176.9,5196.8,5216.8,5236.8,5256.8,5276.8,5296.8,5316.8,5336.7,5356.7,5376.7,5396.7,5416.7,5436.7,5456.7,5476.7,5496.6,5516.6,5536.6,5556.6,5576.6,5596.6,5616.6,5636.5,5656.5,5676.5,5696.5,5716.5,5736.5,5756.5,5776.4,5796.4,5816.4,5836.4,5856.4,5876.4,5896.4,5916.3,5936.3,5956.3,5976.3,5996.3,6016.3,6036.3,6056.2,6076.2,6096.2,6116.2,6136.2,6156.2,6176.2,6196.1,6216.1,6236.1,6256.1,6276.1,6296.1,6316.1,6336,6356,6376,6396,6416,6436,6456,6475.9,6495.9,6515.9,6535.9,6555.9,6575.9,6595.9,6615.9,6635.8,6655.8,6675.8,6695.8,6715.8,6735.8,6755.8,6775.7,6795.7,6815.7,6835.7,6855.7,6875.7,6895.7,6915.6,6935.6,6955.6,6975.6,6995.6,7015.6,7035.6,7055.5,7075.5,7095.5,7115.5,7135.5,7155.5,7175.5,7195.4,7215.4,7235.4,7255.4,7275.4,7295.4,7315.4,7335.3,7355.3,7375.3,7395.3,7415.3,7435.3,7455.3,7475.2,7495.2,7515.2,7535.2,7555.2,7575.2,7595.2,7615.2,7635.1,7655.1,7675.1,7695.1,7715.1,7735.1,7755.1,7775,7795,7815,7835,7855,7875,7895,7914.9,7934.9,7954.9,7974.9,7994.9,8014.9,8034.9,8054.8,8074.8,8094.8,8114.8,8134.8,8154.8,8174.8,8194.7,8214.7,8234.7,8254.7,8274.7,8294.7,8314.7,8334.6,8354.6,8374.6,8394.6,8414.6,8434.6,8454.6,8474.5,8494.5,8514.5,8534.5,8554.5,8574.5,8594.5,8614.4,8634.4,8654.4,8674.4,8694.4,8714.4,8734.4,8754.4,8774.3,8794.3,8814.3,8834.3,8854.3,8874.3,8894.3,8914.2,8934.2,8954.2,8974.2,8994.2,9014.2,9034.2,9054.1,9074.1,9094.1,9114.1,9134.1,9154.1,9174.1,9194,9214,9234,9254,9274,9294,9314,9333.9,9353.9,9373.9,9393.9,9413.9,9433.9,9453.9,9473.8,9493.8,9513.8,9533.8,9553.8,9573.8,9593.8,9613.7,9633.7,9653.7,9673.7,9693.7,9713.7,9733.7,9753.6,9773.6,9793.6,9813.6,9833.6,9853.6,9873.6,9893.6,9913.5,9933.5,9953.5,9973.5,9993.5,10013.5,10033.5,10053.4,10073.4,10093.4,10113.4,10133.4,10153.4,10173.4,10193.3,10213.3,10233.3,10253.3,10273.3,10293.3,10313.3,10333.2,10353.2,10373.2,10393.2,10413.2,10433.2,10453.2,10473.1,10493.1,10513.1,10533.1,10553.1,10573.1,10593.1,10613,10633,10653,10673,10693,10713,10733,10752.9,10772.9,10792.9,10812.9,10832.9,10852.9,10872.9,10892.8,10912.8,10932.8,10952.8,10972.8,10992.8,11012.8,11032.8,11052.7,11072.7,11092.7,11112.7,11132.7,11152.7,11172.7,11192.6,11212.6,11232.6,11252.6,11272.6,11292.6,11312.6,11332.5,11352.5,11372.5,11392.5,11412.5,11432.5,11452.5,11472.4,11492.4,11512.4,11532.4,11552.4,11572.4,11592.4,11612.3,11632.3,11652.3,11672.3,11692.3,11712.3,11732.3,11752.2,11772.2,11792.2,11812.2,11832.2,11852.2,11872.2,11892.1,11912.1,11932.1,11952.1,11972.1,11992.1,12012.1,12032.1,12052,12072,12092,12112,12132,12152,12172,12191.9,12211.9,12231.9,12251.9,12271.9,12291.9,12311.9,12331.8,12351.8,12371.8,12391.8,12411.8,12431.8,12451.8,12471.7,12491.7,12511.7,12531.7,12551.7,12571.7,12591.7,12611.6,12631.6,12651.6,12671.6,12691.6,12711.6,12731.6,12751.5,12771.5,12791.5,12811.5,12831.5,12851.5,12871.5,12891.4,12911.4,12931.4,12951.4,12971.4,12991.4,13011.4,13031.3,13051.3,13071.3,13091.3,13111.3,13131.3,13151.3,13171.3,13191.2,13211.2,13231.2,13251.2,13271.2,13291.2,13311.2,13331.1,13351.1,13371.1,13391.1,13411.1,13431.1,13451.1,13471,13491,13511,13531,13551,13571,13591,13610.9,13630.9,13650.9,13670.9,13690.9,13710.9,13730.9,13750.8,13770.8,13790.8,13810.8,13830.8,13850.8,13870.8,13890.7,13910.7,13930.7,13950.7,13970.7,13990.7,14010.7,14030.6,14050.6,14070.6,14090.6,14110.6,14130.6,14150.6,14170.5,14190.5,14210.5,14230.5,14250.5,14270.5,14290.5,14310.5,14330.4,14350.4,14370.4,14390.4,14410.4,14430.4,14450.4,14470.3,14490.3,14510.3,14530.3,14550.3,14570.3,14590.3,14610.2,14630.2,14650.2,14670.2,14690.2,14710.2,14730.2,14750.1,14770.1,14790.1,14810.1,14830.1,14850.1,14870.1,14890,14910,14930,14950,14970,14990,15010,15029.9,15049.9,15069.9,15089.9,15109.9,15129.9,15149.9,15169.8,15189.8,15209.8,15229.8,15249.8,15269.8,15289.8,15309.7,15329.7,15349.7,15369.7,15389.7,15409.7,15429.7,15449.7,15469.6,15489.6,15509.6,15529.6,15549.6,15569.6,15589.6,15609.5,15629.5,15649.5,15669.5,15689.5,15709.5,15729.5,15749.4,15769.4,15789.4,15809.4,15829.4,15849.4,15869.4,15889.3,15909.3,15929.3,15949.3,15969.3,15989.3,16009.3,16029.2,16049.2,16069.2,16089.2,16109.2,16129.2,16149.2,16169.1,16189.1,16209.1,16229.1,16249.1,16269.1,16289.1,16309,16329,16349,16369,16389,16409,16429,16449,16468.9,16488.9,16508.9,16528.9,16548.9,16568.9,16588.9,16608.8,16628.8,16648.8,16668.8,16688.8,16708.8,16728.8,16748.7,16768.7,16788.7,16808.7,16828.7,16848.7,16868.7,16888.6,16908.6,16928.6,16948.6,16968.6,16988.6,17008.6,17028.5,17048.5,17068.5,17088.5,17108.5,17128.5,17148.5,17168.4,17188.4,17208.4,17228.4,17248.4,17268.4,17288.4,17308.3,17328.3,17348.3,17368.3,17388.3,17408.3,17428.3,17448.2,17468.2,17488.2,17508.2,17528.2,17548.2,17568.2,17588.2,17608.1,17628.1,17648.1,17668.1,17688.1,17708.1,17728.1,17748,17768,17788,17808,17828,17848,17868,17887.9,17907.9,17927.9,17947.9,17967.9,17987.9,18007.9,18027.8,18047.8,18067.8,18087.8,18107.8,18127.8,18147.8,18167.7,18187.7,18207.7,18227.7,18247.7,18267.7,18287.7,18307.6,18327.6,18347.6,18367.6,18387.6,18407.6,18427.6,18447.5,18467.5,18487.5,18507.5,18527.5,18547.5,18567.5,18587.4,18607.4,18627.4,18647.4,18667.4,18687.4,18707.4,18727.4,18747.3,18767.3,18787.3,18807.3,18827.3,18847.3,18867.3,18887.2,18907.2,18927.2,18947.2,18967.2,18987.2,19007.2,19027.1,19047.1,19067.1,19087.1,19107.1,19127.1,19147.1,19167,19187,19207,19227,19247,19267,19287,19306.9,19326.9,19346.9,19366.9,19386.9,19406.9,19426.9,19446.8,19466.8,19486.8,19506.8,19526.8,19546.8,19566.8,19586.7,19606.7,19626.7,19646.7,19666.7,19686.7,19706.7,19726.7,19746.6,19766.6,19786.6,19806.6,19826.6,19846.6,19866.6,19886.5,19906.5,19926.5,19946.5,19966.5,19986.5,20006.5,20026.4,20046.4,20066.4,20086.4,20106.4,20126.4,20146.4,20166.3,20186.3,20206.3,20226.3,20246.3,20266.3,20286.3,20306.2,20326.2,20346.2,20366.2,20386.2,20406.2,20426.2,20446.1,20466.1,20486.1,20506.1,20526.1,20546.1,20566.1,20586,20606,20626,20646,20666,20686,20706,20725.9,20745.9,20765.9,20785.9,20805.9,20825.9,20845.9,20865.9,20885.8,20905.8,20925.8,20945.8,20965.8,20985.8,21005.8,21025.7,21045.7,21065.7,21085.7,21105.7,21125.7,21145.7,21165.6,21185.6,21205.6,21225.6,21245.6,21265.6,21285.6,21305.5,21325.5,21345.5,21365.5,21385.5,21405.5,21425.5,21445.4,21465.4,21485.4,21505.4,21525.4,21545.4,21565.4,21585.3,21605.3,21625.3,21645.3,21665.3,21685.3,21705.3,21725.2,21745.2,21765.2,21785.2,21805.2,21825.2,21845.2,21865.1,21885.1,21905.1,21925.1,21945.1,21965.1,21985.1,22005.1,22025,22045,22065,22085,22105,22125,22145,22164.9,22184.9,22204.9,22224.9,22244.9,22264.9,22284.9,22304.8,22324.8,22344.8,22364.8,22384.8,22404.8,22424.8,22444.7,22464.7,22484.7,22504.7,22524.7,22544.7,22564.7,22584.6,22604.6,22624.6,22644.6,22664.6,22684.6,22704.6,22724.5,22744.5,22764.5,22784.5,22804.5,22824.5,22844.5,22864.4,22884.4,22904.4,22924.4,22944.4,22964.4,22984.4,23004.3,23024.3,23044.3,23064.3,23084.3,23104.3,23124.3,23144.3,23164.2,23184.2,23204.2,23224.2,23244.2,23264.2,23284.2,23304.1,23324.1,23344.1,23364.1,23384.1,23404.1,23424.1,23444,23464,23484,23504,23524,23544,23564,23583.9,23603.9,23623.9,23643.9,23663.9,23683.9,23703.9,23723.8,23743.8,23763.8,23783.8,23803.8,23823.8,23843.8,23863.7,23883.7,23903.7,23923.7,23943.7,23963.7,23983.7,24003.6,24023.6,24043.6,24063.6,24083.6,24103.6,24123.6,24143.6,24163.5,24183.5,24203.5,24223.5,24243.5,24263.5,24283.5,24303.4,24323.4,24343.4,24363.4,24383.4,24403.4,24423.4,24443.3,24463.3,24483.3,24503.3,24523.3,24543.3,24563.3,24583.2,24603.2,24623.2,24643.2,24663.2,24683.2,24703.2,24723.1,24743.1,24763.1,24783.1,24803.1,24823.1,24843.1,24863,24883,24903,24923,24943,24963,24983,25002.9,25022.9,25042.9,25062.9,25082.9,25102.9,25122.9,25142.8,25162.8,25182.8,25202.8,25222.8,25242.8,25262.8,25282.8,25302.7,25322.7,25342.7,25362.7,25382.7,25402.7,25422.7,25442.6,25462.6,25482.6,25502.6,25522.6,25542.6,25562.6,25582.5,25602.5,25622.5,25642.5,25662.5,25682.5,25702.5,25722.4,25742.4,25762.4,25782.4,25802.4,25822.4,25842.4,25862.3,25882.3,25902.3,25922.3,25942.3,25962.3,25982.3,26002.2,26022.2,26042.2,26062.2,26082.2,26102.2,26122.2,26142.1,26162.1,26182.1,26202.1,26222.1,26242.1,26262.1,26282,26302,26322,26342,26362,26382,26402,26422,26441.9,26461.9,26481.9,26501.9,26521.9,26541.9,26561.9,26581.8,26601.8,26621.8,26641.8,26661.8,26681.8,26701.8,26721.7,26741.7,26761.7,26781.7,26801.7,26821.7,26841.7,26861.6,26881.6,26901.6,26921.6,26941.6,26961.6,26981.6,27001.5,27021.5,27041.5,27061.5,27081.5,27101.5,27121.5,27141.4,27161.4,27181.4,27201.4,27221.4,27241.4,27261.4,27281.3,27301.3,27321.3,27341.3,27361.3,27381.3,27401.3,27421.2,27441.2,27461.2,27481.2,27501.2,27521.2,27541.2,27561.2,27581.1,27601.1,27621.1,27641.1,27661.1,27681.1,27701.1,27721,27741,27761,27781,27801,27821,27841,27860.9,27880.9,27900.9,27920.9,27940.9,27960.9,27980.9,28000.8,28020.8,28040.8,28060.8,28080.8,28100.8,28120.8,28140.7,28160.7,28180.7,28200.7,28220.7,28240.7,28260.7,28280.6,28300.6,28320.6,28340.6,28360.6,28380.6,28400.6,28420.5,28440.5,28460.5,28480.5,28500.5,28520.5,28540.5,28560.5,28580.4,28600.4,28620.4,28640.4,28660.4,28680.4,28700.4,28720.3,28740.3,28760.3,28780.3,28800.3,28820.3,28840.3,28860.2,28880.2,28900.2,28920.2,28940.2,28960.2,28980.2,29000.1,29020.1,29040.1,29060.1,29080.1,29100.1,29120.1,29140,29160,29180,29200,29220,29240,29260,29279.9,29299.9,29319.9,29339.9,29359.9,29379.9,29399.9,29419.8,29439.8,29459.8,29479.8,29499.8,29519.8,29539.8,29559.7,29579.7,29599.7,29619.7,29639.7,29659.7,29679.7,29699.7,29719.6,29739.6,29759.6,29779.6,29799.6,29819.6,29839.6,29859.5,29879.5,29899.5,29919.5,29939.5,29959.5,29979.5,29999.4,30019.4,30039.4,30059.4,30079.4,30099.4,30119.4,30139.3,30159.3,30179.3,30199.3,30219.3,30239.3,30259.3,30279.2,30299.2,30319.2,30339.2,30359.2,30379.2,30399.2,30419.1,30439.1,30459.1,30479.1,30499.1,30519.1,30539.1,30559,30579,30599,30619,30639,30659,30679,30698.9,30718.9,30738.9,30758.9,30778.9,30798.9,30818.9,30838.9,30858.8,30878.8,30898.8,30918.8,30938.8,30958.8,30978.8,30998.7,31018.7,31038.7,31058.7,31078.7,31098.7,31118.7,31138.6,31158.6,31178.6,31198.6,31218.6,31238.6,31258.6,31278.5,31298.5,31318.5,31338.5,31358.5,31378.5,31398.5,31418.4,31438.4,31458.4,31478.4,31498.4,31518.4,31538.4,31558.3,31578.3,31598.3,31618.3,31638.3,31658.3,31678.3,31698.2,31718.2,31738.2,31758.2,31778.2,31798.2,31818.2,31838.1,31858.1,31878.1,31898.1,31918.1,31938.1,31958.1,31978.1,31998,32018,32038,32058,32078,32098,32118,32137.9,32157.9,32177.9,32197.9,32217.9,32237.9,32257.9,32277.8,32297.8,32317.8,32337.8,32357.8,32377.8,32397.8,32417.7,32437.7,32457.7,32477.7,32497.7,32517.7,32537.7,32557.6,32577.6,32597.6,32617.6,32637.6,32657.6,32677.6,32697.5,32717.5,32737.5,32757.5,32777.5,32797.5,32817.5,32837.4,32857.4,32877.4,32897.4,32917.4,32937.4,32957.4,32977.4,32997.3,33017.3,33037.3,33057.3,33077.3,33097.3,33117.3,33137.2,33157.2,33177.2,33197.2,33217.2,33237.2,33257.2,33277.1,33297.1,33317.1,33337.1,33357.1,33377.1,33397.1,33417,33437,33457,33477,33497,33517,33537,33556.9,33576.9,33596.9,33616.9,33636.9,33656.9,33676.9,33696.8,33716.8,33736.8,33756.8,33776.8,33796.8,33816.8,33836.7,33856.7,33876.7,33896.7,33916.7,33936.7,33956.7,33976.6,33996.6,34016.6,34036.6,34056.6,34076.6,34096.6,34116.6,34136.5,34156.5,34176.5,34196.5,34216.5,34236.5,34256.5,34276.4,34296.4,34316.4,34336.4,34356.4,34376.4,34396.4,34416.3,34436.3,34456.3,34476.3,34496.3,34516.3,34536.3,34556.2,34576.2,34596.2,34616.2,34636.2,34656.2,34676.2,34696.1,34716.1,34736.1,34756.1,34776.1,34796.1,34816.1,34836,34856,34876,34896,34916,34936,34956,34975.9,34995.9,35015.9,35035.9,35055.9,35075.9,35095.9,35115.8,35135.8,35155.8,35175.8,35195.8,35215.8,35235.8,35255.8,35275.7,35295.7,35315.7,35335.7,35355.7,35375.7,35395.7,35415.6,35435.6,35455.6,35475.6,35495.6,35515.6,35535.6,35555.5,35575.5,35595.5,35615.5,35635.5,35655.5,35675.5,35695.4,35715.4,35735.4,35755.4,35775.4,35795.4,35815.4,35835.3,35855.3,35875.3,35895.3,35915.3,35935.3,35955.3,35975.2,35995.2,36015.2,36035.2,36055.2,36075.2,36095.2,36115.1,36135.1,36155.1,36175.1,36195.1,36215.1,36235.1,36255.1,36275,36295,36315,36335,36355,36375,36395,36414.9,36434.9,36454.9,36474.9,36494.9,36514.9,36534.9,36554.8,36574.8,36594.8,36614.8,36634.8,36654.8,36674.8,36694.7,36714.7,36734.7,36754.7,36774.7,36794.7,36814.7,36834.6,36854.6,36874.6,36894.6,36914.6,36934.6,36954.6,36974.5,36994.5,37014.5,37034.5,37054.5,37074.5,37094.5,37114.4,37134.4,37154.4,37174.4,37194.4,37214.4,37234.4,37254.3,37274.3,37294.3,37314.3,37334.3,37354.3,37374.3,37394.3,37414.2,37434.2,37454.2,37474.2,37494.2,37514.2,37534.2,37554.1,37574.1,37594.1,37614.1,37634.1,37654.1,37674.1,37694,37714,37734,37754,37774,37794,37814,37833.9,37853.9,37873.9,37893.9,37913.9,37933.9,37953.9,37973.8,37993.8,38013.8,38033.8,38053.8,38073.8,38093.8,38113.7,38133.7,38153.7,38173.7,38193.7,38213.7,38233.7,38253.6,38273.6,38293.6,38313.6,38333.6,38353.6,38373.6,38393.5,38413.5,38433.5,38453.5,38473.5,38493.5,38513.5,38533.5,38553.4,38573.4,38593.4,38613.4,38633.4,38653.4,38673.4,38693.3,38713.3,38733.3,38753.3,38773.3,38793.3,38813.3,38833.2,38853.2,38873.2,38893.2,38913.2,38933.2,38953.2,38973.1,38993.1,39013.1,39033.1,39053.1,39073.1,39093.1,39113,39133,39153,39173,39193,39213,39233,39252.9,39272.9,39292.9,39312.9,39332.9,39352.9,39372.9,39392.8,39412.8,39432.8,39452.8,39472.8,39492.8,39512.8,39532.7,39552.7,39572.7,39592.7,39612.7,39632.7,39652.7,39672.7,39692.6,39712.6,39732.6,39752.6,39772.6,39792.6,39812.6,39832.5,39852.5,39872.5,39892.5,39912.5,39932.5,39952.5,39972.4,39992.4,40012.4,40032.4,40052.4,40072.4,40092.4,40112.3,40132.3,40152.3,40172.3,40192.3,40212.3,40232.3,40252.2,40272.2,40292.2,40312.2,40332.2,40352.2,40372.2,40392.1,40412.1,40432.1,40452.1,40472.1,40492.1,40512.1,40532,40552,40572,40592,40612,40632,40652,40672,40691.9,40711.9,40731.9,40751.9,40771.9,40791.9,40811.9,40831.8,40851.8,40871.8,40891.8,40911.8])
print(len(energies))

# Y-axis (counts) is just counts
counts = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,42,361,1521,3174,2917,1491,349,50,10,3,1,1,0,36,41,46,30,45,26,26,38,38,30,41,34,54,59,54,54,86,110,172,144,106,66,55,72,92,94,103,64,72,73,81,101,101,126,93,88,78,70,66,67,139,368,1012,2435,4122,4966,4265,2757,1471,720,372,283,301,884,2988,7562,15318,22802,25017,20035,12327,6237,3079,1701,1013,636,377,230,152,169,167,181,197,159,170,130,158,127,136,149,142,147,166,237,289,427,485,499,498,440,399,357,319,315,316,317,341,323,375,435,591,1027,1848,3109,4827,6377,6924,6098,4712,3516,3046,3317,3808,3997,3836,3487,3341,3559,3956,4064,3646,2775,1963,1303,921,703,612,675,757,805,809,832,921,1143,1643,2162,2560,2578,2240,1629,1165,786,557,542,549,615,617,607,603,658,662,812,898,1161,1415,1579,1611,1381,1124,776,589,497,373,384,402,406,427,423,533,529,544,591,603,580,642,558,576,587,569,517,536,561,576,542,617,646,645,631,735,870,1372,2351,4411,7923,12489,17194,20655,21004,18368,13784,9361,5906,3803,2745,2174,1951,1685,1456,1211,1077,1016,1142,1358,1584,2189,2906,3771,4337,4454,4043,3454,2735,1968,1519,1232,1014,940,923,958,929,934,939,968,1070,1094,1213,1234,1447,1672,2073,2343,2585,2731,2534,2183,1854,1559,1244,1041,1024,1007,1007,996,967,922,948,895,948,1002,1039,1039,1037,1221,1291,1459,1493,1622,1762,1608,1568,1395,1330,1298,1176,1195,1280,1281,1327,1458,1611,1943,2446,3703,6747,14046,28626,54650,95508,148670,206932,254568,278421,270634,234211,178485,122929,75036,41434,21253,10305,5439,3187,2158,1696,1426,1385,1271,1239,1316,1329,1307,1469,1571,1750,1964,2347,3269,4715,7342,11883,18146,25607,33176,39028,41075,38912,33552,26097,17976,11664,6754,3774,2274,1205,846,654,543,490,461,475,565,670,759,811,944,921,861,791,698,616,572,495,492,474,421,462,462,424,440,464,464,514,546,604,578,614,690,680,722,754,783,873,986,1117,1217,1313,1428,1407,1524,1454,1321,1210,1029,918,756,728,598,553,513,507,456,444,452,439,438,487,431,493,471,501,463,548,533,548,504,523,527,550,529,552,595,581,599,661,613,562,607,568,562,547,539,577,549,640,649,723,677,752,695,689,652,677,615,653,631,700,602,617,655,629,613,557,579,556,505,491,547,480,446,486,486,480,466,500,467,509,567,537,556,513,491,550,527,543,502,442,459,473,441,449,449,478,451,501,506,493,463,459,481,472,431,440,424,424,423,439,454,412,418,392,412,414,400,401,420,429,422,419,410,437,412,412,388,386,433,382,422,427,440,450,483,507,639,740,831,906,1016,1153,1140,1031,986,860,787,636,564,490,462,461,440,413,458,427,466,429,450,433,485,477,530,503,503,439,502,448,423,430,416,426,435,434,431,453,419,453,418,461,416,436,376,383,380,402,379,392,352,387,370,400,375,339,365,351,306,345,333,305,279,278,312,347,313,292,287,302,327,331,328,301,309,283,304,300,328,299,299,283,295,305,307,326,362,424,464,624,888,1252,1749,2357,3193,3880,4596,5048,5246,5187,4725,4066,3296,2695,1971,1429,886,634,466,378,324,250,240,251,229,257,234,244,243,252,296,332,388,404,593,697,953,1190,1306,1513,1657,1600,1554,1453,1227,1032,805,606,483,354,274,221,167,158,123,139,107,118,128,106,134,140,121,113,123,142,141,145,159,156,169,167,177,212,177,206,174,171,144,100,138,80,81,92,77,66,72,90,92,84,66,81,63,85,78,74,67,68,60,51,46,44,58,49,39,42,40,35,32,28,35,49,36,31,32,23,40,32,33,31,29,31,28,27,27,32,43,33,24,39,50,48,32,33,35,50,35,27,28,41,35,39,31,38,32,31,23,25,37,25,31,28,33,32,33,40,27,19,31,23,22,37,27,23,33,24,25,36,27,24,26,38,39,31,22,27,21,20,28,23,26,24,39,19,27,24,20,36,27,32,25,28,33,23,20,19,19,29,22,20,22,29,17,25,20,29,24,33,21,24,25,18,27,27,19,17,30,25,19,21,19,25,22,19,15,33,18,31,24,32,30,23,20,28,20,28,27,33,34,32,21,28,27,22,22,26,18,19,22,16,19,20,19,15,26,23,26,23,22,21,22,14,27,17,27,19,26,26,21,21,25,23,24,18,14,18,22,11,24,12,23,23,25,23,16,18,18,18,18,15,19,8,12,18,15,14,23,16,11,16,9,20,9,27,15,17,23,17,11,19,13,15,19,16,13,12,17,16,18,17,12,23,34,36,48,45,53,60,69,61,61,41,58,51,47,40,22,23,31,15,11,18,13,12,13,12,11,8,6,9,11,12,12,17,16,18,25,21,29,35,39,36,33,33,24,26,23,13,24,10,11,10,10,6,8,5,11,5,7,6,11,4,6,1,7,2,5,7,7,13,6,6,4,11,9,9,5,11,6,7,8,3,3,4,2,7,4,3,3,2,1,1,0,2,0,1,2,4,4,3,2,0,2,2,1,0,3,0,2,1,4,1,3,1,0,0,1,2,6,1,1,2,0,3,2,2,1,0,0,1,1,0,1,1,0,1,1,0,0,2,1,0,3,1,2,1,1,0,0,1,1,2,1,0,0,0,0,0,1,0,1,1,0,3,0,1,0,1,0,2,1,0,1,1,0,0,0,0,1,0,0,0,1,0,1,1,1,0,2,1,1,0,1,0,0,2,2,2,2,2,1,0,0,0,1,1,1,0,1,1,0,0,1,0,0,2,5,0,0,2,0,0,1,1,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,1,0,0,0,2,1,0,0,0,0,3,2,0,1,0,0,0,1,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,2,0,0,0,0,0,1,1,0,0,1,1,0,0,0,2,0,0,1,0,0,0,0,0,1,1,0,0,0,1,0,2,0,0,0,1,2,0,0,0,0,0,0,1,0,3,0,1,0,1,1,1,0,0,1,1,2,0,1,2,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
print(len(counts))

# Make Dataframe
raw_dict = {'Energy':energies, 'Counts':counts}
raw_df = pd.DataFrame(data=raw_dict)
print(raw_df)



# Attempt 2 using scipy and seaborn
p_height_min = None  # Required height of peaks. 0.5% of max?
p_threshhold = None  # Required threshold of peaks, the vertical distance to its neighboring samples. Shouldn't use for XRF spectra, in case peak is between two bins.
p_prominence = max(counts)*0.0006 # Required prominence of peaks. try 0.1% of max count? otherwise ~400
print(f'p_prominence={p_prominence}')
p_distance_min = 4  # horizontal distance between two peaks
found_peak_indexes, found_peaks_properties = sig.find_peaks(x=counts, height=p_height_min, threshold=p_threshhold, distance=p_distance_min, prominence=p_prominence)

print(found_peaks_properties)
peak_df = raw_df.iloc[found_peak_indexes].reset_index()
left_bases = raw_df.iloc[found_peaks_properties['left_bases']]['Energy'].to_numpy()
right_bases = raw_df.iloc[found_peaks_properties['right_bases']]['Energy'].to_numpy()
print(right_bases)

peak_df['Left Peak Base Energy'] = left_bases
peak_df['Right Peak Base Energy'] = right_bases

print(peak_df)

#peak_energies = found_peaks

# print(peak_energies)
# peak_counts = []
# for peak in peak_energies:
#     peak_counts.append(np.where(energies==peak)[0])

# peaks_dict = {'Energy':peak_energies, 'Counts':peak_counts}
#  peak_df = pd.DataFrame(data=peaks_dict)





plt.scatter(x=peak_df['Energy'], y=peak_df['Counts'], color='red',alpha=0.6, picker=5)
plt.plot(raw_df['Energy'], raw_df['Counts'])



plt.show()





# # Attempt 1
# 
# # try to get delta array
# counts_delta = []
# for i in range(len(counts)):
#     try:
#         counts_delta.append(counts[i]-counts[i-1])
#     except:
#         counts_delta.append(0)
# # print(counts_delta)
# counts_delta = np.array(counts_delta)
# peak_energies = []
# i = 0
# previous_cd = 0
# for i in range(len(counts_delta)):
#         if (counts_delta[i] > 0) and (counts_delta[i+1] < 0) and counts[i]>600 and (counts_delta[i]-counts_delta[i+1]>170):
#             peak_energies.append(energies[i])
#             plt.axvline(x = energies[i], color = 'g', ymin=0, linestyle = 'dashed', linewidth= '1', label = energies[i])
#             plt.text(energies[i],0,energies[i],rotation=270,rotation_mode='anchor', color='g', size=8)
# plt.plot(energies, counts)
# plt.plot(energies, counts_delta)
# #plt.legend()
# print(peak_energies)
# plt.show()