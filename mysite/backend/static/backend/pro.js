var pro = (function (layui) {

    var $ = layui.jquery;
    var layer = layui.layer;
    var laypage = layui.laypage;


    /*********数据表格选择************/
        //所有被选中的id
    var primaryArray = [];
    $('.primary').click(function () {
        if ($(this).is(":checked")) {
            primaryArray.push(parseInt($(this).attr('data-id')));
        } else {
            deleteElem(primaryArray, parseInt($(this).attr('data-id')));
        }
    });
    $('.allSelect').click(function(){
        if ($(this).is(":checked")) {
            $(this).parents('table').find('tbody').children('tr').each(function (index) {
                $(this).find('td').find('input').prop('checked','checked');
                primaryArray.push(parseInt($(this).attr('id')));
            })
        } else {
            $(this).parents('table').find('tbody').children('tr').each(function (index) {
                $(this).find('td').find('input').removeProp('checked');
                deleteElem(primaryArray, parseInt($(this).attr('id')));
            })
        }
    });


    //删除数组中某个指定元素，应用操作
    function deleteElem(arr, elem) {
        var len = arr.length;
        for (var i = 0; i < len; i++) {
            if (arr[i] == elem) {
                arr.splice(i, 1);
            }
        }
    }

    //js数组去重
    function arrayUnique(array){
        var temp = [];
        for(var i = 0; i < array.length; i++){
            if(temp.indexOf(array[i]) == -1){
                temp.push(array[i]);
            }
        }
        return temp;
    }

    //暴露的方法
    var getPrimaryKey = function (one) {
        if (primaryArray.length < 1) {
            layer.alert('没有选择任何数据');
            return false;
        }
        if (primaryArray.length == 1) {
            return primaryArray[0]
        }
        //只返回最后一个id
        if(one){
            return primaryArray.pop();
        }
        primaryArray = arrayUnique(primaryArray);
        return primaryArray.join(',');
    };


    /*********左侧菜单************/
    zhedie();

    function zhedie() {
        $('.layui-nav-tree li').each(function (index) {
            if ($(this).find('dd').hasClass('layui-this')) {
                $(this).addClass('layui-nav-itemed').siblings().removeClass('layui-nav-itemed');
            }
        });
    }


    /****************分页相关****************/
    //获取分页相关信息
    laypage.limit = $('#page').attr('data-perPage');
    laypage.curr = $('#page').attr('data-nowPage');
    laypage.count = $('#page').attr('data-total');
    //分页
    laypage.render({
        elem: 'page',
        limit: laypage.limit,
        curr: laypage.curr,
        count: laypage.count,
        jump: function (obj, first) {
            //首次不执行
            if (!first) {
                laypage.location(obj.curr);
            }
        }
    });
    //跳转方法
    laypage.location = function (curr) {
        var url = '';
        var href = window.location.href;
        if (href.indexOf('?') != -1) {
            if (/page=\d+/.test(href)) {
                url = href.replace(/page=\d+/, 'page=' + curr);
            } else {
                url = href + '&page=' + curr;
            }
        } else {
            url = href + '?page=' + curr;
        }
        window.location = url;
    };


    /*********点击按钮************/
    var message = function (message, url, primary) {
        layer.confirm(message, {
            btn: ['确定', '取消'] //按钮
        }, function () {
            toAjax(url, primary);
        }, function () {
            //取消，不做任何操作
        });
    };

    var dialog = function (title, url, area) {
        layer.open({
            type: 2,
            title: title,
            shadeClose: true,
            shade: false,
            maxmin: false, //开启最大化最小化按钮
            // area: ['400px', '500px'],
            area: area,
            content: url
        });
    };


    /********dialog相关**********/
    //点击确定和关闭按钮
    $('.ok').click(function(){

        var url = $('#form').attr('data-action');
        //数据验证，调用iframe页面的验证方法
        var error = checkForm();
        if(error){
            layer.alert(error);
            return false;
        }

        //数据
        var data = $('#form').serializeArray();

        //ajax提交
        toAjaxInDialog(url,data);

    });
    $('.no').click(function(){
        closeSelf();
        return false;
    });


    /*************模块部分树状菜单*************/
    //TODO
    //有bug
    $('.moduleTree').click(function(){
        $(this).find('img').toggleClass('treeDown');
        var module_id = parseInt($(this).attr('data-id'));
        toHide(module_id,$(this));
    });

    function toHide(module_id,obj){
        if(obj){
            var finalObj;
            var final_module_id;
            obj.parents('tr').nextAll().each(function(index){
                var pid = parseInt($(this).find('td').eq(3).text());
                if(pid == module_id){
                    //获取当前层级最后一个tr的module_id
                    final_module_id = parseInt($(this).find('td').eq(1).text());
                    //获取当前层级最后一个tr的点击对象
                    finalObj = $(this).find('td').eq(2);
                    $(this).toggleClass('treeHide');
                    toHide(final_module_id,finalObj);
                }
            });
        }else{
            return false;
        }
    }




    /****************辅助方法****************/
    function toAjax(url, data) {
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            datatype: 'json',
            success: function (res) {
                var res = eval('(' + res + ')');
                if (res.status != 100) {
                    layer.alert(res.msg);
                    return false;
                } else {
                    //操作成功，关闭并刷新
                    layer.close(layer.index);
                    window.history.go(0);
                }
            },
            error: function () {
                layer.alert('请求出错');
            }
        });
    }

    function toAjaxInDialog(url, data) {
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            datatype: 'json',
            success: function (res) {
                var res = eval('(' + res + ')');
                if (res.status != 100) {
                    layer.alert(res.msg);
                } else {
                    //操作成功，关闭当前ifram
                    closeSelf();
                    flushTop();
                }
            },
            error: function () {
                layer.alert('请求出错');
            }
        });
    }

    //关闭自己
    function closeSelf(){
        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
        parent.layer.close(index); //再执行关闭
    }
    //刷新父级
    function flushTop(){
        parent.location.reload();
    }

    //判断一个元素是否在一个数组中，不在的话就将它加入到数组中去
    function joinToArray(array,elem){
        var flag = 0;
        for(i in array){
            if(array[i] == elem){
                flag = 1;
            }
        }
        if(flag == 0){
            array.push(elem);
        }
        //无需return，push方法直接操作原数据
    }
    //判断一个元素是否在一个数组中，在的话就将它截去
    function subToArray(array,elem){
        var flag = 0;
        var index = 0;
        for(i in array){
            if(array[i] == elem){
                flag = 1;
                index = i;
            }
        }
        if(flag == 1){
            array.splice(index,1);
        }
    }

    function layerAlert(msg){
        layer.alert(msg);
    }

    function layerLoad(type){
        return layer.load(type);
    }

    function layerClose(index){
        layer.close(index);
    }




    /*******暴露出来的方法*********/
    return {
        joinToArray:joinToArray,
        subToArray:subToArray,
        getPrimaryKey: getPrimaryKey,
        message: message,
        dialog: dialog,
        alert:layerAlert,
        load:layerLoad,
        closeLayer:layerClose,
    }


})(layui);