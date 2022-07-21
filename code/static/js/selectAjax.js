(function () {
    var stations;
    var lightStation;

    //加载网页时 请求所有stations信息 添加到地图/添加name到select
    $.ajax({
        type: 'GET',
        url: "http://127.0.0.1:5000/getAllStationInfo",
        dataType: 'json',
        data: {},// 这次请求要携带的数据
        success: function (res) {
            const data = res;
            var objString = JSON.stringify(data);
            var objJson = JSON.parse(objString);
            nameList = objJson.names;//station的名字
            latList = objJson.lats;//station的纬度
            lonList = objJson.lons;//station的经度

            //加载station下拉框
            var strStationOption = '';
            for (var i = 0; i < nameList.length; i++) {
                var opt = '<option id=\"'+ i +'\"'+ ' value=\"' + nameList[i] + '\">' + nameList[i] + '</option>';
                strStationOption += opt;
            }
            $('#station').html(strStationOption);


            //加载staion到map    
            stations = L.layerGroup();
            for (var i = 0; i < nameList.length; i++) {
                L.marker([latList[i], lonList[i]],{highlight: 'temporary'}).bindPopup(nameList[i]).addTo(stations);
                
            }
            
            //设置底图
            var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '@ OpenStreetMap'
            });
            var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
            var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
            var streets = L.tileLayer(mbUrl, {
                id: 'mapbox/streets-v11',
                tileSize: 512,
                zoomOffset: -1,
                attribution: mbAttr
            });
            var satellite = L.tileLayer(mbUrl, {
                id: 'mapbox/satellite-v9',
                tileSize: 512,
                zoomOffset: -1,
                attribution: mbAttr
            });

            //定义地图容器
            var map = L.map('map', {
                center: [45.450859, 9.206543],
                zoom: 7,
                layers: [osm, stations]//m默认加载
            });

            //分组1
            var baseLayers = {
                'OpenStreetMap': osm,
                'Streets': streets,
                'Satellite': satellite
            };

            //分组2
            var overlays = {
                'Stations': stations
            };

            //添加control到map
            var layerControl = L.control.layers(baseLayers, overlays).addTo(map);

            //添加弹出
            var popup = L.popup();
            function onMapClick(e) {
                //alert(e.latlng.lat)
                popup
                    .setLatLng(e.latlng)
                    .setContent("You clicked the map at " + e.latlng.toString())
                    .openOn(map);
            }        
            
            lightStation=1;
            highlightStation(1);

            //map.on('click', onMapClick);

            //添加 dem
            $.ajax({
                type: 'GET',
                url: "http://127.0.0.1:5000/getDEM",
                dataType: 'json',
                data: {},// 这次请求要携带的数据
                success: function (res) {
                    const data = res;
                    var objString = JSON.stringify(data);
                    var objJson = JSON.parse(objString);
                    latLngBounds = objJson.bounds;

                    var imageUrl = '../static/images/DEM_WGS84_SPINO.png';
                    var imageOverlay = L.imageOverlay(imageUrl, latLngBounds, {
                        opacity: 0.7,
                        interactive: true
                    }).addTo(map);

                    // L.rectangle(latLngBounds).addTo(map);
                    // map.fitBounds(latLngBounds);
                }
            })


        }
    })



    /*查询 某个station 在 某个时间段内的 ztd*/
    $('#submit1').on('click', function () {
        $.ajax({
            type: 'GET',
            url: "http://127.0.0.1:5000/getOneStation",
            dataType: 'json',
            data: {
                'station': $('#station').val(),
                'sdate': $('#sdate').val(),
                'stime': $('#stime').val(),
                'ssecond': $('#ssecond').val(),
                'edate': $('#edate').val(),
                'etime': $('#etime').val(),
                'esecond': $('#esecond').val(),

            },// 这次请求要携带的数据
            success: function (res) {
                //alert('success')
                //console.log(json.parse(JSON.stringify(res)));

                const data = res;
                var objString = JSON.stringify(data);
                var objJson = JSON.parse(objString);
                datelist = objJson.date;
                valuelist = objJson.values;

                //渲染到表格
                var strTable = '';
                strTable += '<tr><th>Number</th><th>Date</th><th>ZTD(m)</th></tr>';
                for (var i = 0; i < datelist.length; i++) {
                    var tds = '<tr><td>'+ i + '</td><td>'+ datelist[i] + '</td><td>' + valuelist[i] + '</td></tr>';
                    strTable += tds;
                }
                //alert(strTable)
                $('#dataTable').html(strTable);



                //渲染到echarts
                var dom = document.getElementById('container');
                var myChart = echarts.init(dom, null, {
                    renderer: 'canvas',
                    useDirtyRect: false
                });

                var option;

                option = {
                    // Make gradient line here
                    visualMap: {
                        show: false,
                        type: 'continuous',
                        seriesIndex: 0,
                        min: 0,
                        max: 100000000000
                    },
                    title: {
                        left: 'center',
                        text: 'ZTDs values in ' + $('#station').val()
                    },
                    legend: {
                        data: ['ZTD']
                    },
                    tooltip: {
                        trigger: 'axis',
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        name: 'DateTime',
                        nameTextStyle: { // x轴name的样式调整
                            color: 'black',
                            fontSize: 18,
                        },
                        nameGap: 30,  // x轴name与横坐标轴线的间距
                        nameLocation: "middle", // x轴name处于x轴的什么位置
                        type: 'category',
                        data: datelist
                    },
                    yAxis: {
                        name: 'ZTD(m)',
                        nameTextStyle: {  // y轴name的样式调整
                            color: 'black',
                            fontSize: 18,
                        },
                        nameRotate: 90, // y轴name旋转90度 使其垂直
                        nameGap: 50,  // y轴name与横纵坐标轴线的间距
                        nameLocation: "middle", // y轴name处于y轴的什么位置
                        type: 'value',
                        min: function (value) { return value.min; },
                        max: function (value) { return value.max; },
                        interval: 0.01,
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '8%',
                        containLabel: true
                    },
                    dataZoom: [
                        {
                            type: 'inside',
                            xAxisIndex: 0,
                            filterMode: 'none'
                        },
                        {
                            type: 'inside',
                            yAxisIndex: 0,
                            filterMode: 'none'
                        },
                        {
                            type: 'inside',
                            start: 0,
                            end: 10
                        },
                        {
                            start: 0,
                            end: 10
                        }
                    ],
                    series: [
                        {
                            type: 'line',
                            symbol: 'none',
                            symbol: 'none',
                            lineStyle: {
                                normal: {
                                    color: 'red',
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: 'rgb(255, 70, 131)'
                                },
                            },
                            areaStyle: {},
                            showSymbol: false,
                            data: valuelist
                        }
                    ]
                };
                if (option && typeof option === 'object') {
                    myChart.setOption(option);
                }

                window.addEventListener('resize', myChart.resize);
            }//success

        })//ajax

    })//click


    document.getElementById("station").onchange = function () { myFunction() };

    function myFunction() {
        var x = document.getElementById("station");
        highlightStation(x.selectedIndex + 1)
        
    }

    function highlightStation(sid){
        stations.getLayer(lightStation).disablePermanentHighlight();
        stations.getLayer(lightStation).closePopup();
        lightStation=sid;
        stations.getLayer(sid).enablePermanentHighlight();
        stations.getLayer(sid).openPopup();
    }


})();

