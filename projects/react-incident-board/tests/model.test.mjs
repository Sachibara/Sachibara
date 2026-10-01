import test from 'node:test';
import assert from 'node:assert/strict';
import {parseIncidents,transition} from '../src/model.ts';
const item={id:'1',title:'Test incident',priority:'High',status:'New',created:'2026-10-01T00:00:00Z'};
test('backup round-trip preserves records',()=>assert.deepEqual(parseIncidents(JSON.stringify([item])),[item]));
test('invalid and duplicate imports are rejected',()=>{for(const data of [[{...item,status:'Unknown'}],[item,item],[{...item,title:''}],[{...item,created:'bad'}],{}])assert.throws(()=>parseIncidents(JSON.stringify(data)));});
test('transition is immutable and only changes target',()=>{const original=[item,{...item,id:'2'}];const changed=transition(original,'1','Resolved');assert.equal(changed[0].status,'Resolved');assert.equal(original[0].status,'New');assert.equal(changed[1],original[1]);assert.throws(()=>transition(original,'1','Invalid'));});
