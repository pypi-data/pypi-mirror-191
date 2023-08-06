import{_ as o,d as t,w as i,n as s,y as n}from"./c.a24dad9a.js";import"./c.fef57cf6.js";import{o as e}from"./index-0cebb5a2.js";import{o as a}from"./c.bc0ca5c5.js";import"./c.2fd5868c.js";import"./c.abbbe9de.js";let c=class extends s{render(){return n`
      <esphome-process-dialog
        .heading=${`Clean ${this.configuration}`}
        .type=${"clean"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_openInstall(){e(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],c.prototype,"configuration",void 0),c=o([i("esphome-clean-dialog")],c);
