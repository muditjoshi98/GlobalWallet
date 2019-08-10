import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'urls.dart';

class Register extends StatefulWidget {

  @override
  _RegisterState createState() => _RegisterState();
}

class _RegisterState extends State<Register> {
  BuildContext scaffoldContext;
  var userNameController = TextEditingController();

  var passwordController = TextEditingController();

  var nameController = TextEditingController();

  var emailController = TextEditingController();

  void register(BuildContext context) async{
    String userName = userNameController.text+"@globalWallet";
    String password = passwordController.text;
    String name = nameController.text;
    String email = emailController.text;
    String url = Urls.registerApi;
    var response = await http.post(url,body: {'uid':userName,'name':name,'password':password,'email':email});
    final Map parsed = json.decode(response.body);
    if(parsed["message"] == "SUCCESS"){
      Navigator.of(context).pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Global Wallet::Register"),
      ),
      body: SingleChildScrollView(
        child:Container(
          padding: EdgeInsets.all(10),
          child: Column(children: <Widget>[
            SizedBox(height: 60,),
            TextField(decoration: InputDecoration(labelText: "Username"),
            controller: userNameController,),
            TextField(decoration: InputDecoration(labelText: "Password"),
            obscureText: true,
            controller: passwordController,),
            TextField(decoration: InputDecoration(labelText: "Name"),
            controller: nameController,),
            TextField(decoration: InputDecoration(labelText: "Email"),
            keyboardType: TextInputType.emailAddress,
            controller: emailController,),
            SizedBox(height: 30,),
            RaisedButton(child: Text("Register"),
            onPressed:()=> register(context),)

          ],),
        ),    
    ),
    );
  }
}