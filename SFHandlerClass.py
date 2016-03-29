import sys

class SFYaml:
   
   sectioncount = 0
   
   YAMLSECTION = "---"

   header = {}

   def stripkey(self, line):
      line = line.strip()
      line = line.replace('- ', '')
      return line

   def stripvalue(self, line):
      line = line.strip()
      line = line.lstrip("'").rstrip("'")
      return line

   def handleentry(self, line):
      line = line.split(':', 1)
      line[0] = self.stripkey(line[0])
      line[1] = self.stripvalue(line[1])
      return line

   def sfaslist(self, sfname):
      with open(sfname, 'rb') as sfile:
         for line in sfile: 
            line = line.strip()
            if line == self.YAMLSECTION:
               self.sectioncount += 1 
            if self.sectioncount == 1:
               if line != self.YAMLSECTION:
                  line = self.handleentry(line)
                  self.header[line[0]] = line[1]

      print self.header
