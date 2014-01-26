module Jekyll
  class Vimeo < Liquid::Tag

    def initialize(name, id, tokens)
      super
      @id, @args = id.split(" ", 2)
    end

    def render(context)
      %(<div class="embed-video-container"><iframe src="http://player.vimeo.com/video/#{@id}" #{@args}></iframe></div>)
    end
  end
end

Liquid::Template.register_tag('vimeo', Jekyll::Vimeo)
