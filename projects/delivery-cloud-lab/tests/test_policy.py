import unittest
from policy import review
class PolicyTests(unittest.TestCase):
 def test_open_ssh_is_rejected(self):
  p={'resource_changes':[{'address':'sg','type':'aws_security_group','change':{'after':{'ingress':[{'protocol':'tcp','from_port':22,'to_port':22,'cidr_blocks':['0.0.0.0/0']}]}}}]}
  self.assertEqual(len(review(p)['findings']),1)
 def test_private_ssh_and_deleted_resources(self):
  p={'resource_changes':[{'type':'aws_security_group','change':{'after':{'ingress':[{'protocol':'tcp','from_port':22,'to_port':22,'cidr_blocks':['10.0.0.0/8']}]}}},{'type':'aws_instance','change':{'after':None}}]}
  self.assertEqual(review(p)['findings'],[])
 def test_public_storage_check(self):
  p={'resource_changes':[{'type':'aws_s3_bucket_public_access_block','change':{'after':{'block_public_acls':False}}}]}
  self.assertEqual(len(review(p)['findings']),1)
if __name__=='__main__':unittest.main()
