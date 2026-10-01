/* Script Include: ChangePolicy. Global application; Client callable = false. */
var ChangePolicy = Class.create();
ChangePolicy.prototype = {
    initialize: function() {},
    canTransition: function(from, to, risk, hasPlan, isApprover) {
        var paths = {draft:['approved','rejected'],approved:['implemented'],rejected:[],implemented:[]};
        if (!paths[from] || paths[from].indexOf(to) === -1) return false;
        if ((to === 'approved' || to === 'rejected') && !isApprover) return false;
        if (to === 'approved' && risk === 'high' && !hasPlan) return false;
        return true;
    },
    type: 'ChangePolicy'
};
