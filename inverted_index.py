__author__ = 'Qing'
# -*- coding: UTF-8 -*-
from bson.code import Code
from pymongo import MongoClient
from datetime import *

mapper = Code("""
    function(){
        for(var i=0; i< this.content_arr.length; i++){
            sentence = this.content_arr[i];
            if(sentence.length<2){
                continue;
            }
            var reg = /^.*[~!“’□《》（）@#\$%\^&\*\(\)_+\-=\[\]\{\}\\\|\'\";:,\<\.\>\/\?\s+].*$/;
            if(reg.test(sentence)){
                continue;
            }
            if(sentence.match(/\d/)!=null || sentence.match(/[a-zA-Z]/)!=null ){
                continue;
            }

            sentence_start = this.content.indexOf(sentence)
            for(var idx = 0;idx <sentence.length-1 ; idx++) {
                word = sentence.substring(idx,idx+2);
                value = {arr:[{"position":idx+sentence_start,"sentence_index":i, "poem_id":this._id}]}
                emit(word,value);
            }

            if(sentence.length >2){
                for(var idx = 0;idx <sentence.length-2; idx++) {
                    word = sentence.substring(idx,idx+3);
                    value = {arr:[{"position":idx+sentence_start,"sentence_index":i, "poem_id":this._id}]}
                    emit(word,value);
                }
            }
        };
    }
""")

reducer = Code("""
    function(key, values){
        reduced = {arr :[],count:0}
        for (var i =0;i<values.length; i++){
            for(j=0; j< values[i].arr.length;j++){
                reduced.arr.push(values[i].arr[j]);
            }
        }
        return reduced;
    }
""")

if __name__ == "__main__":
    client = MongoClient("127.0.0.1", 27017)
    db = client.ts_db
    print("start time " + str(datetime.today()))
    result = db.ts_co2.map_reduce(mapper, reducer, "inverted_index")
    #
    # for doc in result.find():
    #     print(doc)

    print("end time " + str(datetime.today()))
