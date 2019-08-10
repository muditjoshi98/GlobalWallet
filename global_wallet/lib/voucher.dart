import 'package:flutter/material.dart';

class Voucher extends StatelessWidget {
  final Function openWalletSelectionPage;
  final String text;
  Voucher(this.text, this.openWalletSelectionPage);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap:()=> openWalletSelectionPage(text, context),
          child: Container(
        color: Colors.lightBlue,
        margin: EdgeInsets.all(5),
        height:100,
        width: 100,
        child: Center(
          child: Text(text,
        style: TextStyle(color: Colors.black,
        fontSize: 30,),),
      ),),
    );
  }
}