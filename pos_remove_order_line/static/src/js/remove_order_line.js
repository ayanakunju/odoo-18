/** @odoo-module */
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

patch(Orderline.prototype, {
    setup() {
        super.setup();
        this.numberBuffer = useService("number_buffer");
        console.log('ssssssssss', this.numberBuffer)
    },
    async removeLine() {
        this.numberBuffer.sendKey('Backspace');
        this.numberBuffer.sendKey('Backspace');
    }
})


//patch(Orderline.prototype, {
//    async removeLine() {
//      const order = this.env.services.pos.get_order();
//        const orderline = order.orderlines.find((line) => line.full_product_name == this.props.line.productName);
//        return order.removeOrderline(orderline);
//
//    }
//});
