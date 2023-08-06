from . import AbstractParser
from ...models import AnnotationTarget



class ItemProp(AbstractParser):
    def parse(self, annotation_target: AnnotationTarget, target_url, bs_document, previous_parse_result):
        # Does not change result if previous parse match
        # if previous_parse_result:
        #     return previous_parse_result
        if annotation_target.publication_date is None:
            date_published_element = bs_document.select("[itemProp='datePublished']")
            if date_published_element :
                content = date_published_element[0]["content"]
                if content:
                    annotation_target.publication_date = content
                else :
                    datetime = date_published_element[0]["datetime"]
                    if datetime:
                        annotation_target.publication_date = datetime

        if annotation_target.image is None:
            image_element = bs_document.select("[itemProp='image']")
            if image_element:
                image_element_url = image_element[0]["src"]
                if image_element_url:
                    annotation_target.image = image_element_url

        return True
