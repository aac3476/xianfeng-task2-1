from flask import Flask,render_template,request
import pymysql
import json

app = Flask(__name__)

@app.route('/')
def search():
    return(render_template('search.html'))


@app.route('/test')
def test():
    return (render_template('result.html'))


@app.route('/result', methods=['POST'])
def result():
    print(request.form['search'])
    heroname = request.form['search']
    if(heroname == ''):
        error = 1
        return (render_template('search.html') )
    db = pymysql.connect("188.131.175.223", "username", "password", "wzrytest", charset='utf8')
    cursor = db.cursor()
    sql = r"select * from herolist where name like '%"+heroname+"%'"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        '''
        for row in results:
            bigname = row[2]
            shengcun = row[3]
            gongji = row[4]
            jinengxiaohao = row[5]
            shangshou = row[6]
            bgpic = row[7]
            jineng = row[8]
            equip = row[9]
            # 打印结果
            print
            "fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
            (fname, lname, age, sex, income)
            '''
    except:
        return (render_template('search.html',error =1))

    if(results.__len__()<=0):
        return (render_template('search.html', error=1))

    row = results[0][8]
    print(results[0])
    jineng = row.split('|')

    jinenglist=[]
    for xx in jineng:
        if xx == '':
            continue

        sql = r"select * from jinenglist where id = "+str(xx)
        try:
            cursor.execute(sql)
            jinengres = cursor.fetchall()
            seq = ('id','name','lengque','xiaohao','dec1','tip','pic')
            jinengdict = dict.fromkeys(seq,jinengres)
            seq = ('id','name','lengque','xiaohao','dec1','tip','pic')

            jinengdict = dict.fromkeys(seq)
            jinengdict['id']=jinengres[0][0]
            jinengdict['name'] = jinengres[0][1]
            jinengdict['lengque'] = jinengres[0][2]
            jinengdict['xiaohao'] = jinengres[0][3]
            jinengdict['dec1'] = jinengres[0][4]
            jinengdict['tip'] = jinengres[0][5]
            jinengdict['pic'] = jinengres[0][6]
            jinenglist.append(jinengdict)
        except:
            return (render_template('search.html', error=1))
        if (jinengres.__len__() <= 0):
            return (render_template('search.html', error=1))
        #print(jinengres)
    # 关闭数据库连接
    db.close()
    print(jinenglist)
    res = list(results)
    floatlist = []
    floatlist.append(float(res[0][3]))
    floatlist.append(float(res[0][4]))
    floatlist.append(float(res[0][5]))
    floatlist.append(float(res[0][6]))
    return(render_template('index.html',hero=res[0],jineng=jinenglist,floatlist=floatlist))


if __name__ == '__main__':
    app.run(host='0.0.0.0')