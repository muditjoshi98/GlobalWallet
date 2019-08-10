import 'package:flutter/material.dart';
import 'WalletSelectionPage.dart';
import 'quick_vouchers.dart';
import 'SendWalletSelectionPage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'urls.dart';
import 'transactions.dart';

class MyHomePage extends StatefulWidget {
  final String id;
  MyHomePage(this.id);
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var amountController = TextEditingController();

  Future<String> getBalance() async{
    String url = Urls.getBalanceApi+widget.id;
    var response = await http.get(url);
    print(response.body);
    final Map parsed =json.decode(response.body);
    double bal=parsed["data"];
    return "Balance: "+bal.toString();
  }

  void openWalletSelectionPage(String amount, BuildContext context){
    if(amount.isEmpty){
      return;
    }
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => WalletSelectionPage(amount, widget.id)),);
  }

  void openWalletSendSelectionPage(String amount, BuildContext context){
    if(amount.isEmpty){
      return;
    }
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => SendWalletSelectionPage(amount, widget.id)),);
  }

  void openTransactionsPage(BuildContext context){
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => Transactions(widget.id)),);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Global Wallet"),
      ),
      body: SingleChildScrollView(
        child:Container(
          padding: EdgeInsets.all(10),
          child: Column(children: <Widget>[    
            SizedBox(height: 10,),
            FutureBuilder<String>(
              future: getBalance(),
              builder: (context,balance){
                return Text(balance.data,style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),);
              },),
            SizedBox(height: 30,),
            Container(child: Text("Quick Vouchers",style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),), alignment: Alignment.center,),
            QuickVouchers(openWalletSelectionPage),
            SizedBox(height: 10,),
            Divider(height: 2,),
            SizedBox(height: 30,),
            Container(child:new TextField(decoration: InputDecoration(labelText: "Enter Amount"),controller: amountController,keyboardType: TextInputType.number,),),
            SizedBox(height: 10,),
            RaisedButton(
              color: Colors.lightBlue,
              child: Text("Recharge",style: TextStyle(color: Colors.black,fontWeight: FontWeight.bold,),),
              onPressed: ()=>openWalletSelectionPage(amountController.text, context),),
              RaisedButton(
              color: Colors.lightBlue,
              child: Text("Send",style: TextStyle(color: Colors.black,fontWeight: FontWeight.bold,),),
              onPressed: ()=>openWalletSendSelectionPage(amountController.text,context),),
              RaisedButton(
              color: Colors.lightBlue,
              child: Text("History",style: TextStyle(color: Colors.black,fontWeight: FontWeight.bold,),),
              onPressed: ()=>openTransactionsPage(context),)
    ],crossAxisAlignment: CrossAxisAlignment.end,),
        ),
        
    ),
    );
  }
}