import thing
import command

def numbered(strs):
    return ("{0}. {1}".format(num+1, line) 
            for num, line in enumerate(strs))

@thing.facet_classes.register
class HelpFacet(thing.ThingFacet):
    name = "help"
    commands = command.thing.create_child_set(name)
    
    short_template = "\"{0}\"" 
    full_template = short_template + ": {1}"
    
    @classmethod
    def does_attach(cls, thing):
        return True
    
    def get_topics(self, thing):
        topics = dict()
        for facet in thing.facets.itervalues():
            for commandset in (facet.commands, facet.listens):
                if commandset:
                    for command in commandset:
                        if command.visible:
                            topic = command.format.replace("{thing}", thing.name)
                            help  = command.help.replace("{thing}", thing.name) 
                            topics[topic] = help
        return topics
    
    def format_help(self, thing, full=False):
        line_template = self.full_template if full else self.short_template 
        help_lines = [line_template.format(topic, help) 
                      for topic, help in self.get_topics(thing).items()]
        help_lines.sort()
        return help_lines
    
    @commands.add("help {thing}", help="view command help for {thing}")
    def help(self, thing, context):
        context.reply("Commands: " + ", ".join(self.format_help(thing)))
        
    @commands.add("help {thing} {topic}", help="view help for {topic} on {thing}")
    def help_topic(self, thing, topic, context):
        topic = topic.strip("\"")
        topics = self.get_topics(thing)
        if topic in topics:
            context.reply(self.full_template.format(topic, topics[topic]))
        else:
            context.reply("I know of no such help topic.")