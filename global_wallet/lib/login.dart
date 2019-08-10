import 'package:flutter/material.dart';
import 'package:global_wallet/MyHomePage.dart';
import 'package:global_wallet/register.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'urls.dart';

class Login extends StatefulWidget {
  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
  var userNameController = TextEditingController();

  var passwordController = TextEditingController();

  void login(BuildContext context) async{
    String userName = userNameController.text;
    String password = passwordController.text;
    if(!userName.contains("@globalWallet")){
      userName+="@globalWallet";
    }
    //API Call
    String url = Urls.loginApi;
    var response = await http.post(url,body: {'uid':userName,'password':password});
    final Map parsed = json.decode(response.body);
    if(parsed["message"] == "SUCCESS"){
      Navigator.push(context,
      MaterialPageRoute(builder: (c)=>MyHomePage(userName)));
    }
  }

  void openRegister(BuildContext context){
    Navigator.push(context,
    MaterialPageRoute(builder: (c)=>Register()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Global Wallet::Login"),
      ),
      body: SingleChildScrollView(
        child:Container(
          padding: EdgeInsets.all(10),
          child: Column(children: <Widget>[
            SizedBox(height: 100,),
            TextField(decoration: InputDecoration(labelText: "Username"),
            controller: userNameController,),
            TextField(decoration: InputDecoration(labelText: "Password",),
            obscureText: true,
            controller: passwordController,),
            SizedBox(height: 30,),
            RaisedButton(child: Text("Login"),
            onPressed:()=> login(context),),
            RaisedButton(child: Text("Register"),
            onPressed:()=> openRegister(context),)

          ],),
        ),    
    ),
    );
  }
}