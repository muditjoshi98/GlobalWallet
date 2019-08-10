import 'package:flutter/material.dart';
import 'voucher.dart';

class QuickVouchers extends StatelessWidget {
  final Function openWalletSelectionPage;
  final List<String> vouchers = ["10", "50", "100", "500", "1000", "10000"];
  QuickVouchers(this.openWalletSelectionPage);

  @override
  Widget build(BuildContext context) {
    return Container(
      height:150,
          child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Container(
            margin: EdgeInsets.all(10),
            child: Row(
              children: <Widget>[
                ...vouchers.map((voucher) {
                  return Voucher(voucher, openWalletSelectionPage);
                }).toList(),
              ],
            )),
      ),
    );
  }
}
