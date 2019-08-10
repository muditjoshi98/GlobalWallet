import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'urls.dart';

class NewTransactionSend extends StatefulWidget {
  final String id;
  final String service;
  final String merchant;
  final String image;
  final String amount;

  NewTransactionSend(this.service,this.image,this.merchant,this.amount,this.id);

  @override
  _NewTransactionSendState createState() => _NewTransactionSendState();
}

class _NewTransactionSendState extends State<NewTransactionSend> {
  final userIdController = TextEditingController();

  void _Pay() async{
    String userId = userIdController.text;
    String amount = widget.amount;
    String id = widget.id;
    String service = widget.service;
    String merchant = widget.merchant;
    
    if (userId.isEmpty){
      return;
    }
    if(service=="Global Wallet" && !userId.contains("@globalWallet")){
      userId+="@globalWallet";
    }
    //API Call here
    String url=Urls.sendApiOther;
    if(service=="Global Wallet"){
      url=Urls.sendApiGlobal;
    }
    var response = await http.post(url,body:{'sender_id':id,'receiver_id':userId,'amount':amount});
    final Map parsed = json.decode(response.body);
    if(parsed["message"]=="SUCCESS"){
      Navigator.of(context).pop();
      Navigator.of(context).pop();
    }
    
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
          child: Container(
        margin: EdgeInsets.symmetric(
          horizontal: 10,
          vertical: 5,
        ),
        padding: EdgeInsets.all(6),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: <Widget>[
          SizedBox(height: 30,),
          ListTile(title: Text(widget.service),leading: CircleAvatar(child: Image.asset(widget.image,fit: BoxFit.cover,),backgroundColor: Colors.white,),),
          TextField(
            decoration: InputDecoration(labelText: widget.service+" ID"),
            controller: userIdController,
          ),
          TextField(
            decoration: InputDecoration(labelText: "MerchantId"),
            enabled: false,
            controller: TextEditingController(text: widget.merchant),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Amount"),
            enabled: false,
            controller: TextEditingController(text: widget.amount),
          ),
          SizedBox(height: 20,),
          Container(
            margin: EdgeInsets.only(top:6,),
            decoration: BoxDecoration(
              color: Theme.of(context).primaryColor,
              border: Border.all(width:2,color:Theme.of(context).primaryColorDark,),
            ),
            child: 
            FlatButton(
            child: Text("Send Money",
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: Colors.white,
              fontSize: 15,
            ),),
            onPressed:()=> _Pay(),
          ),
          ),
        ],)
      ),
    );
  }
}