import asyncio, os, unittest
from uuid import uuid4
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from ops.graph import make_builder, Request
from pydantic import ValidationError

class WorkflowTests(unittest.IsolatedAsyncioTestCase):
 async def execute(self,request):
  graph=make_builder().compile(checkpointer=InMemorySaver()); config={'configurable':{'thread_id':str(uuid4())}}
  result=await graph.ainvoke({'request':request},config)
  return graph,config,result
 async def test_approval_and_calculation(self):
  g,c,r=await self.execute({'quantity':40,'discount':12})
  self.assertTrue(r['__interrupt__']); self.assertEqual(r['quote']['total_cents'],1017280); self.assertNotIn('reply',r)
  result=await g.ainvoke(Command(resume={'action':'approve','quote_id':r['quote']['id']}),c)
  self.assertEqual(result['status'],'approved'); self.assertIn('draft',result['reply'])
 async def test_decline(self):
  g,c,r=await self.execute({'quantity':40,'discount':12})
  result=await g.ainvoke(Command(resume={'action':'reject','quote_id':r['quote']['id']}),c)
  self.assertEqual(result['status'],'rejected')
 async def test_tampered_approval(self):
  g,c,r=await self.execute({'quantity':40,'discount':12})
  with self.assertRaises(ValueError): await g.ainvoke(Command(resume={'action':'approve','quote_id':'wrong'}),c)
 async def test_unavailable_and_alternative(self):
  g,c,r=await self.execute({'quantity':80,'discount':12})
  self.assertEqual(r['status'],'blocked'); self.assertNotIn('__interrupt__',r); self.assertEqual(r['alternatives'][0]['id'],'form-chair')
 async def test_compliant(self):
  g,c,r=await self.execute({'quantity':12,'discount':5,'product_id':'rise-desk','deadline_days':7})
  self.assertEqual(r['status'],'ready'); self.assertEqual(r['quote']['total_cents'],625860)
 def test_input_validation(self):
  for bad in [{'quantity':-1},{'discount':99},{'quantity':1.5},{'product_id':'invented'},{'approved':True}]:
   with self.assertRaises(ValidationError): Request.model_validate(bad)
if __name__=='__main__': unittest.main()
