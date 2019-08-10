import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'urls.dart';
import 'history_item.dart';
import 'package:intl/intl.dart';

class Transactions extends StatefulWidget {
  final String id;
  Transactions(this.id);

  @override
  _TransactionsState createState() => _TransactionsState();
}

class _TransactionsState extends State<Transactions> {

  Future<List<HistoryItem>> fetchTransactions() async{
    String url = Urls.historyApi+widget.id;
    var response = await http.get(url);
    final Map<String,dynamic> parsed = json.decode(response.body);
    final List<dynamic> p = parsed["data"];
    List<HistoryItem> hList = [];
    for(var i in p){
      Map<String,dynamic> m = i;
      print(m["add"]);
      print(m["service"]);
      HistoryItem h = HistoryItem(
        add: m["add"],
        amount: m["amount"],
        other_id: m["other_id"],
        user_id: m["user_id"],
        timestamp: m["timestamp"],
        id: m["id"],
        service: m["service"]);
      hList.add(h);
    }
    return hList;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Global Wallet::History"),
      ),
      body: Container(
        height: MediaQuery.of(context).size.height,
        child: FutureBuilder(future: fetchTransactions(),
        builder: (context,r){
          return ListView(children: <Widget>[
            ...(r.data as List<HistoryItem>).map((h){
              return Card(
                color: h.add=="True"?Colors.lightGreen:Colors.redAccent,
                              child: ListTile(
                  title: Text(h.other_id),
                  leading: CircleAvatar(child: FittedBox(child:Text(h.amount, textAlign: TextAlign.center,),),radius: 40,),
                  subtitle: Text(h.service+"\n"+h.timestamp),
                ),
              );
            }).toList(),
          ],);
        },),
      ),);
  }
}