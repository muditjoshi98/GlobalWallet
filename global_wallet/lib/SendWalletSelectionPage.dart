import 'package:flutter/material.dart';
import 'package:global_wallet/new_transaction_send.dart';

class SendWalletSelectionPage extends StatelessWidget {

  final String amount;
  final String id;
  SendWalletSelectionPage(this.amount, this.id);
  final List<List<String>> wallets = [
    ["Global Wallet", "lib/images/global-wallet.png", "GlobalWalletMerchantId"], 
    ["Paytm", "lib/images/paytm-logo.jpg", "PaytmMerchantId"], 
    ["Amazon Pay", "lib/images/amazon-pay.jpg", "AmazonPayMerchantId"], 
    ["Google Pay", "lib/images/google-pay.png", "GooglePayMerchantId"],
    ["PhonePe", "lib/images/phonepe.jpeg", "PhonePeMerchantId"]];

  void showAppModal(String service, String image, String merchant, BuildContext context){
    showModalBottomSheet(context: context,
    builder: (bctx)=>NewTransactionSend(service,image,merchant,amount,id),
    isScrollControlled: true,
    elevation: 10,);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Global Wallet::Send Money"),
      ),
      body: SingleChildScrollView(
        child:Container(
          height:MediaQuery.of(context).size.height,
          padding: EdgeInsets.all(10),
          child: ListView(children: <Widget>[
            ...wallets.map((wallet){
              return ListTile(title: Text(wallet[0]),leading: CircleAvatar(child: Image.asset(wallet[1],fit: BoxFit.cover,),backgroundColor: Colors.white,)
              ,onTap:()=> showAppModal(wallet[0],wallet[1],wallet[2],context),);
            }),
          ],),
        ),    
    ),
    );
  }
}