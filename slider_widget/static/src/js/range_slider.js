/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class RangeSliderField extends Component {
  static template = 'FieldRangeSlider';
  setup(){
       const {min,max} = this.__owl__.parent.props.fieldInfo.attrs
       this.state = useState({
           value : this.props.record.data[this.props.name],
           min : min,
           max : max,
       });
  }
  getValue(e) {
       const config = this.env.model.config
       this.state.value = e.srcElement.value
       console.log(this.state.value)
       console.log('stateeeeeeeeeeeee',this.state)
       this.env.model.orm.write(config.resModel,[config.resId], {
                               [this.props.name]: this.state.value,});

  }
}
export const rangeSliderField = {
              component: RangeSliderField,
              displayName: "RangeSliderField",
              supportedTypes: ["int"],
              };
registry.category("fields").add("RangeSliderField", rangeSliderField);
