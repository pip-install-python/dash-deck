import React from 'react';
import Deck from "deck.gl"
import { StaticMap } from "react-map-gl";
import {JSONConverter} from '@deck.gl/json';
import {CSVLoader} from "@loaders.gl/csv";
import {registerLoaders} from "@loaders.gl/core";
import {
  MapView, 
  FirstPersonView, 
  OrthographicView, 
  OrbitView
} from '@deck.gl/core';

import * as layers from "@deck.gl/layers";
import * as aggregationLayers from "@deck.gl/aggregation-layers"
import * as geoLayers from "@deck.gl/geo-layers";
import * as meshLayers from "@deck.gl/mesh-layers";
import PropTypes from 'prop-types';


// CSV loader is needed to download and read CSV Files
registerLoaders(CSVLoader);
// Configure the JSON converter to include all possible
// layers and views.
const configuration = {
  classes: Object.assign(
    {}, 
    layers, 
    aggregationLayers,
    geoLayers,
    meshLayers,
    {
      MapView, 
      FirstPersonView, 
      OrthographicView, 
      OrbitView
    }
  ),
}
const jsonConverter = new JSONConverter({ configuration });


/**
 * This component lets you visualizes PyDeck and deck/json files
 * directly in Dash. It also exposes various events (such as click,
 * hover and drag) inside callbacks.
 */
export default class DeckGL extends React.Component {
    render() {
      let {data} = this.props;
      const {id, mapboxKey} = this.props;

      // If data is a string, we need to convert into JSON format
      if (typeof(data) === "string"){
        data = JSON.parse(data);
      }
      // Now, we can convert the JSON document to a deck object
      const deckProps = jsonConverter.convert(data);

      // Assign the ID to the deck object
      deckProps.id = id;

      // Extract the map style from JSON document, since the map style 
      // is sometimes located in data.views.length
      if (!("mapStyle" in deckProps) && "views" in data && data.views.length > 0){
        deckProps.mapStyle = data.views[0].mapStyle;
      }

      // Only render static map if a mapbox token was given
      let staticMap;
      if (mapboxKey !== null){
        staticMap = <StaticMap
          mapboxApiAccessToken={mapboxKey}
          mapStyle={deckProps.mapStyle}
        />
      } else {
        staticMap = null;
      }

      return (
          <Deck
              onClick={(clickInfo, clickEvent) => this.props.setProps({clickInfo, clickEvent})}
              onDragStart={(dragStartInfo, dragStartEvent) => this.props.setProps({dragStartInfo, dragStartEvent})}
              onDragEnd={(dragEndInfo, dragEndEvent) => this.props.setProps({dragEndInfo, dragEndEvent})}
              onHover={(hoverInfo, hoverEvent) => this.props.setProps({hoverInfo, hoverEvent})}
              {...deckProps}
          >
            {staticMap}
          </Deck>
      );
    }
}

DeckGL.defaultProps = {
    data: {},
    mapboxKey: null
};

DeckGL.propTypes = {
    /**
     * Your map using the Deck.gl JSON format. This can be generated by calling
     * pdk.Deck(...).to_json(). Both a Python dictionary and a JSON-string your map is accepted.
     */
    data: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),


    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,


    /**
     * `mapboxKey` (text): You will need a mapbox token to use deck.gl. Please create a mapbox
     * and follow the instructions here: https://docs.mapbox.com/help/how-mapbox-works/access-tokens/
     */
    mapboxKey: PropTypes.string,


    /**
     * Read-only prop. This prop is updated when an element in the map is clicked. This contains
     * the original gesture event (in JSON).
     */
    clickEvent: PropTypes.object,


    /**
     * Read-only prop. This prop is updated when an element in the map is clicked. This contains
     * the picking info describing the object being clicked.
     * 
     * Complete description here:
     * https://deck.gl/docs/developer-guide/interactivity#the-picking-info-object
     */
    clickInfo: PropTypes.object,


    /**
     * Read-only prop. This prop is updated when an element in the map is hovered. This contains
     * the original gesture event (in JSON).
     */
    hoverEvent: PropTypes.object,


    /**
     * Read-only prop. This prop is updated when an element in the map is hovered. This contains
     * the picking info describing the object being hovered.
     * 
     * Complete description here:
     * https://deck.gl/docs/developer-guide/interactivity#the-picking-info-object
     */
    hoverInfo: PropTypes.object,

    /**
     * Read-only prop. This prop is updated when the user starts dragging on the canvas. This contains
     * the original gesture event (in JSON).
     */
    dragStartEvent: PropTypes.object,


    /**
     * Read-only prop. This prop is updated when the user starts dragging on the canvas. This contains
     * the picking info describing the object being dragged.
     * 
     * Complete description here:
     * https://deck.gl/docs/developer-guide/interactivity#the-picking-info-object
     */
    dragStartInfo: PropTypes.object,


    /**
     * Read-only prop. This prop is updated when the user releases from dragging the canvas. This contains
     * the original gesture event (in JSON).
     */
    dragEndEvent: PropTypes.object,


    /**
     * Read-only prop. This prop is updated when the user releases from dragging the canvas. This contains
     * the picking info describing the object being dragged.
     * 
     * Complete description here:
     * https://deck.gl/docs/developer-guide/interactivity#the-picking-info-object
     */
    dragEndInfo: PropTypes.object,


    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
