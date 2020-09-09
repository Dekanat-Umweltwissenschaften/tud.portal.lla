import DateTime
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavigationRoot
from tud.portal.lla.tile import ITile
from tud.portal.lla.tilepage import ITilePage
from plone import api
from Products.Five import BrowserView

class TilePageView(BrowserView):

    def _getTileWidth(self, brainTile):
        if hasattr(brainTile.getObject(), 'width'):
            return int(brainTile.getObject().width.replace("/3", ""))
        else:
            return 1

    def getPortalURL(self):
        return api.portal.get().absolute_url()

    def isTile(self, obj):
        return ITile.providedBy(obj)

    def tiles(self):
        """Return a catalog search result of tiles to show."""

        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        tiles = catalog(
            object_provides=[ITile.__identifier__, ITilePage.__identifier__],
            path={
                'query': '/'.join(context.getPhysicalPath()),
                'depth': 1
                },
            sort_on='getObjPositionInParent'
            )


        # resort the tiles to fit in the grid
        tiles = tiles.slice(0, len(tiles))

        # in case we find events, we display them as a first item later
        events = self.getEvents()
        place_left = 2 if events else 3

        sorted_tiles = []
        current_set = []
        tiles_len = None
        while len(tiles) > 0:
            if place_left == 0 or len(tiles) == tiles_len:
                # we don't have the right tiles to fill the set
                # begin a new set
                place_left = 3
                sorted_tiles.append(current_set)
                current_set = []
            else:
                tiles_len = len(tiles)

            for i in range(len(tiles)):
                # loop the tiles and find the next fitting tile
                if self._getTileWidth(tiles[i]) <= place_left:
                    place_left = place_left - self._getTileWidth(tiles[i])
                    current_set.append(tiles[i])
                    tiles.pop(i)
                    break

        if len(current_set) > 0:
            sorted_tiles.append(current_set)

        return sorted_tiles

    def getEvents(self):
        # hack to only display events on the front page
        if not self.isFrontPage():
            return []

        catalog = api.portal.get_tool(name='portal_catalog')

        context_helper = getMultiAdapter((self.context, self.request), name="plone_context_state")
        canonical = context_helper.canonical_object()

        start = DateTime.DateTime() - 1  # yesterday
        date_range_query = {'query': [start], 'range': 'min'}

        events = catalog(
            portal_type="Event",
            review_state="published",
            sort_on="start",
            start=date_range_query,
            sort_limit=10,
            path='/'.join(canonical.getPhysicalPath())
            )

        return events

    def parentIsRoot(self):
        context = aq_inner(self.context)
        parent = context.aq_parent
        return INavigationRoot.providedBy(parent)

    def isFrontPage(self):
        # Get path with "Default content item" wrapping applied
        context_helper = getMultiAdapter((self.context, self.request), name="plone_context_state")
        canonical = context_helper.canonical_object()

        return INavigationRoot.providedBy(canonical)


    def tilePageDepth(self):
        context = aq_inner(self.context)
        iter = context.aq_parent
        
        depth = 0
        
        while iter is not None:
            if INavigationRoot.providedBy(iter):
                break
            if ITilePage.providedBy(iter):
                depth = depth+1
            if not hasattr(iter, "aq_parent"):
                raise RuntimeError("Parent traversing interrupted by object: " + str(iter))
            iter = iter.aq_parent
        
        return depth
        
    def parentColor(self):
        context = aq_inner(self.context)
        iter = context.aq_parent
        color = None

        while iter is not None:
            if ITilePage.providedBy(iter) and iter.color != None:
                color = iter.color
                break
            if INavigationRoot.providedBy(iter):
                break
            if not hasattr(iter, "aq_parent"):
                raise RuntimeError("Parent traversing interrupted by object: " + str(iter))
            iter = iter.aq_parent
        
        return color
        
    def color(self):
        context = aq_inner(self.context)
        
        if context.color != None:
            return context.color
        
        return self.parentColor()
        
    def imageDetails(self):
        context = aq_inner(self.context)
        
        if context.image != None:
            iter = context
        else:
            iter = context.aq_parent
            while iter is not None:
                if ITilePage.providedBy(iter) and iter.image != None:
                    break
                if INavigationRoot.providedBy(iter):
                    return None
                    break
                if not hasattr(iter, "aq_parent"):
                    raise RuntimeError("Parent traversing interrupted by object: " + str(iter))
                iter = iter.aq_parent
            
        scales = iter.restrictedTraverse('@@images')
        image_scaled = scales.scale('image', width=1140, height=200, direction='down')
        url = None
        if image_scaled:
            url = image_scaled.url
            
        image_large = scales.scale('image', width=1000, height=700, direction='keep')
        largeUrl = None
        largeWidth = 0
        largeHeight = 0
        if image_large:
            largeUrl = image_large.url
            largeWidth = image_large.width
            largeHeight = image_large.height
        
        copyright = iter.image_copyright
        
        return { 'url': url, 'copyright': copyright, 'largeUrl': largeUrl, 'largeWidth': largeWidth, 'largeHeight': largeHeight }
                
    def siblings(self):
        context = aq_inner(self.context)
        parent = context.aq_parent
        
        if INavigationRoot.providedBy(parent):
            return []
            
        catalog = api.portal.get_tool(name='portal_catalog')
        
        siblings = catalog(
            object_provides=[ITilePage.__identifier__],
            path={
                'query': '/'.join(parent.getPhysicalPath()),
                'depth': 1
                },
            sort_on='getObjPositionInParent'
            )
        
        return siblings