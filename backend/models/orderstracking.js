const mongoose = require('mongoose');

const OrderTrackingSchema = new mongoose.Schema({
    order_id:{
        type:String,
        required:true,
    },
    status:{
        type:String,
        required:true,
    }
}
)

module.exports = mongoose.model('OrderTracking', OrderTrackingSchema);