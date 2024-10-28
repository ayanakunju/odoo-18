/** @odoo-module */
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";

patch( PosOrderline.prototype, {
    removeLine() {
      const order = this.env.services.pos.get_order();

        const orderline = order.orderlines.find((line) => line.full_product_name == this.props.line.productName);

        return order.removeOrderline(orderline);

    }
});

//patch(ProductScreen.prototype, {
//    ClearAll(){
//    const order = this.env.services.pos.get_order();
//    console.log(order)
//    if (order.orderlines.length > 0) {
//      for (let i = order.orderlines.length - 1; i >= 0; i--) {
//        order.removeOrderline(order.orderlines.at(i));
//      }
//    }
//  },
//});

///** @odoo-module */
//import { useService } from "@web/core/utils/hooks";
//import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
//import { patch } from "@web/core/utils/patch";
//import { usePos } from "@point_of_sale/app/store/pos_hook";
//
//patch(Orderline.prototype, {
//    setup() {
//        super.setup();
//        this.pos = usePos();
//        this.numberBuffer = useService("number_buffer");
//        console.log('numberBufferrr',this.numberBuffer)
//    },
//
//    async clear_button_fun(ev) {
//        this.numberBuffer.sendKey('Backspace');
//        this.numberBuffer.sendKey('Backspace');
//    }
//})
