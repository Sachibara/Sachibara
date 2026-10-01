import test from 'node:test';import assert from 'node:assert/strict';import vm from 'node:vm';import {readFileSync} from 'node:fs';
const context={Class:{create:()=>function(){}}};vm.createContext(context);vm.runInContext(readFileSync(new URL('../scripts/ChangePolicy.js',import.meta.url),'utf8'),context);
const policy=new context.ChangePolicy();
test('approval requires role and high-risk rollback plan',()=>{assert.equal(policy.canTransition('draft','approved','high',false,true),false);assert.equal(policy.canTransition('draft','approved','high',true,true),true);assert.equal(policy.canTransition('draft','approved','low',true,false),false);});
test('terminal states and skipped approval are rejected',()=>{assert.equal(policy.canTransition('draft','implemented','low',true,true),false);assert.equal(policy.canTransition('implemented','draft','low',true,true),false);assert.equal(policy.canTransition('approved','implemented','low',true,false),true);});
